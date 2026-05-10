# CCTV AI Implementation Guide - Jetson Orin Nano
## PT CSA (TBG Project) - 40 Cameras Across 10 Sites

---

## 1. HARDWARE ARCHITECTURE

### Current Setup
- **NVR**: Uniview NVR301-04S3-P4 (4-channel PoE NVR)
- **Cameras**: IPC322LB-SF2840 (2MP Bullet, H.265, RTSP)
- **AI Edge**: Jetson Orin Nano Super 8GB (67 TOPS, 1024-core Ampere GPU)
- **Scale**: 10 sites × 4 cameras = 40 cameras total

### Performance Reality Check
**1 Jetson Orin Nano 8GB CANNOT handle 40 streams simultaneously**

Based on benchmarks:
- YOLOv11n TensorRT: ~80-120 FPS single stream (640×640)
- With 4 streams @ 15 FPS each = 60 FPS total inference load
- DeepStream overhead + face recognition + grass monitoring = additional 30-40% load
- **Realistic capacity: 4-6 streams per Jetson @ 10-15 FPS**

### Recommended Architecture
```
Option A (Cost-Optimized):
├── 8× Jetson Orin Nano 8GB (1 per site for 4 cameras)
├── Total: ~$1,600-2,000 hardware
└── Each Jetson handles 4 local cameras

Option B (Centralized):
├── 2× Jetson AGX Orin 32GB (150 TOPS each)
├── Total: ~$3,000-3,500 hardware
└── Each AGX handles 20 cameras @ 8-10 FPS

Option C (Hybrid - RECOMMENDED):
├── 4× Jetson Orin Nano 8GB (1 per 2-3 sites)
├── Network: 1Gbps LAN between sites
└── Each Jetson handles 10 cameras @ 6-8 FPS
```

**For this guide: Option A (1 Jetson per site)**

---

## 2. JETSON ORIN NANO SETUP

### 2.1 Flash JetPack 6.2 (Required for Orin Nano Super)

```bash
# On host PC (Ubuntu 20.04/22.04)
sudo apt update
sudo apt install -y python3-pip python3-venv

# Download NVIDIA SDK Manager
wget https://developer.nvidia.com/sdk-manager
chmod +x sdk-manager-*.run
sudo ./sdk-manager-*.run

# Select: JetPack 6.2, Jetson Orin Nano Super Developer Kit
# Follow on-screen flashing instructions
```

### 2.2 Post-Flash Configuration

```bash
# SSH into Jetson
ssh jetson@<jetson-ip>

# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    vim \
    curl \
    wget \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libimage-exiftool-perl \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libatlas-base-dev \
    gfortran

# Check CUDA version
nvcc --version
# Expected: CUDA 12.x

# Check cuDNN
cat /usr/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
# Expected: cuDNN 9.x

# Check TensorRT
python3 -c "import tensorrt; print(tensorrt.__version__)"
# Expected: TensorRT 10.x
```

### 2.3 Create Python Environment

```bash
cd /home/jetson
python3 -m venv cctv-ai
source cctv-ai/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install PyTorch (JetPack 6.2 includes compatible version)
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Verify GPU access
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
# Expected: CUDA available: True
```

---

## 3. UNIVIEW RTSP STREAM INTEGRATION

### 3.1 Camera RTSP URL Format

Uniview cameras use standard RTSP format:

```
# Main stream (H.265, high quality)
rtsp://<username>:<password>@<camera-ip>:554/unicast/c1/s0/live

# Sub stream (H.264, lower quality - RECOMMENDED for AI)
rtsp://<username>:<password>@<camera-ip>:554/unicast/c1/s1/live
```

### 3.2 Enable RTSP on Uniview NVR

```
1. Access NVR web interface (default: http://<nvr-ip>)
2. Login (default: admin / <password>)
3. Go to: Settings > Network > RTSP
4. Enable RTSP service (port 554)
5. Set RTSP authentication: Digest
6. Note camera IPs from: Settings > Camera > Camera List
```

### 3.3 Test RTSP Stream

```bash
# Install VLC for testing
sudo apt install -y vlc

# Test stream (replace credentials)
vlc rtsp://admin:password@192.168.1.10:554/unicast/c1/s1/live

# Or use ffprobe for stream info
ffprobe -rtsp_transport tcp -i "rtsp://admin:password@192.168.1.10:554/unicast/c1/s1/live"
```

### 3.4 RTSP Connection Pool (Python)

```python
# rtsp_manager.py
import cv2
import threading
from typing import Dict, Optional
import time

class RTSPManager:
    def __init__(self, reconnect_delay: int = 5):
        self.streams: Dict[str, cv2.VideoCapture] = {}
        self.reconnect_delay = reconnect_delay
        self.lock = threading.Lock()
    
    def add_stream(self, stream_id: str, rtsp_url: str) -> bool:
        """Add RTSP stream with automatic reconnection"""
        try:
            cap = cv2.VideoCapture(rtsp_url)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if not cap.isOpened():
                return False
            
            self.streams[stream_id] = cap
            return True
        except Exception as e:
            print(f"Failed to add stream {stream_id}: {e}")
            return False
    
    def get_frame(self, stream_id: str) -> Optional:
        """Get latest frame from stream"""
        with self.lock:
            if stream_id not in self.streams:
                return None
            
            cap = self.streams[stream_id]
            ret, frame = cap.read()
            
            if not ret:
                # Attempt reconnection
                cap.release()
                time.sleep(self.reconnect_delay)
                cap.open(cap.get(cv2.CAP_PROP_URI))
                return None
            
            return frame
    
    def remove_stream(self, stream_id: str):
        """Remove and cleanup stream"""
        with self.lock:
            if stream_id in self.streams:
                self.streams[stream_id].release()
                del self.streams[stream_id]
    
    def cleanup(self):
        """Release all streams"""
        for stream_id in list(self.streams.keys()):
            self.remove_stream(stream_id)
```

---

## 4. AI MODEL SELECTION & DEPLOYMENT

### 4.1 Intrusion Detection - YOLOv11n

**Why YOLOv11n:**
- Fastest inference on Jetson (80-120 FPS @ 640×640)
- Better accuracy than YOLOv8n (mAP +2.1%)
- Native TensorRT support via Ultralytics
- Smaller model size (2.6MB vs 6.2MB for YOLOv8m)

**Installation:**

```bash
source ~/cctv-ai/bin/activate
pip install ultralytics
```

**Model Export to TensorRT:**

```python
# export_model.py
from ultralytics import YOLO

# Load pretrained model
model = YOLO('yolo11n.pt')

# Export to TensorRT (FP16 for Jetson)
model.export(
    format='engine',
    imgsz=640,
    device=0,
    half=True,  # FP16
    workspace=4,  # 4GB max workspace
    simplify=True,
    dynamic=False,
    optimize=True  # Optimize for Jetson
)

# Output: yolo11n.engine
```

**Intrusion Detection Logic:**

```python
# intrusion_detector.py
import cv2
import numpy as np
from ultralytics import YOLO
from shapely.geometry import Polygon, Point

class IntrusionDetector:
    def __init__(self, model_path: str, confidence: float = 0.5):
        # Load TensorRT model
        self.model = YOLO(model_path)
        self.confidence = confidence
        
        # Define restricted zones (polygon coordinates)
        # Format: [(x1,y1), (x2,y2), ...] per camera
        self.restricted_zones: Dict[str, Polygon] = {}
    
    def set_restricted_zone(self, camera_id: str, zone_coords: list):
        """Set restricted zone for camera"""
        self.restricted_zones[camera_id] = Polygon(zone_coords)
    
    def detect_intrusion(self, frame: np.ndarray, camera_id: str) -> list:
        """Detect intrusions in restricted zone"""
        results = self.model(frame, conf=self.confidence, verbose=False)[0]
        
        intrusions = []
        
        if camera_id not in self.restricted_zones:
            return intrusions
        
        zone = self.restricted_zones[camera_id]
        
        for box in results.boxes:
            if results.names[int(box.cls)] not in ['person']:
                continue
            
            # Get box center point
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            center = Point((x1 + x2) / 2, (y1 + y2) / 2)
            
            # Check if center is inside restricted zone
            if zone.contains(center):
                intrusions.append({
                    'type': 'person',
                    'confidence': float(box.conf[0]),
                    'bbox': [x1, y1, x2, y2],
                    'timestamp': time.time()
                })
        
        return intrusions
```

### 4.2 Grass Monitoring - Custom YOLOv11n Segmentation

**Problem:** No pretrained grass height model exists. Must train custom model.

**Approach:**
- Use YOLOv11n-seg (instance segmentation)
- Train on grass texture/height indicators
- Alternative: Use grass coverage % as proxy for "needs mowing"

**Dataset Collection:**

```bash
# Create dataset structure
mkdir -p grass-dataset/{train,val}/images
mkdir -p grass-dataset/{train,val}/labels

# Capture images from CCTV cameras at different grass states
# Label with roboflow or CVAT
```

**Roboflow Dataset Options:**
- https://universe.roboflow.com/search?q=class:grass
- GrassClover Dataset: https://vision.eng.au.dk/grass-clover-dataset/
- Custom: Capture 500+ images per site across seasons

**Training:**

```python
# train_grass.py
from ultralytics import YOLO

# Load segmentation model
model = YOLO('yolo11n-seg.pt')

# Train on custom dataset
model.train(
    data='grass-dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device=0,
    workers=8,
    optimizer='SGD',
    lr0=0.01,
    lrf=0.1,
    momentum=0.937,
    weight_decay=0.0005,
    warmup_epochs=3.0,
    warmup_momentum=0.8,
    warmup_bias_lr=0.1,
    patience=50,
    project='grass-monitoring',
    name='grass-v1'
)

# Export to TensorRT
model.export(format='engine', imgsz=640, device=0, half=True)
```

**Grass Monitoring Logic:**

```python
# grass_monitor.py
import cv2
import numpy as np
from ultralytics import YOLO

class GrassMonitor:
    def __init__(self, model_path: str, threshold: float = 0.7):
        self.model = YOLO(model_path)
        self.threshold = threshold
        
        # Grass coverage thresholds (adjust per site)
        # If grass coverage > threshold, trigger "needs mowing"
        self.mow_thresholds: Dict[str, float] = {}
    
    def set_mow_threshold(self, camera_id: str, threshold: float):
        """Set grass coverage threshold for camera view"""
        self.mow_thresholds[camera_id] = threshold
    
    def analyze_grass(self, frame: np.ndarray, camera_id: str) -> dict:
        """Analyze grass state in frame"""
        results = self.model(frame, verbose=False)[0]
        
        # Calculate grass coverage percentage
        frame_area = frame.shape[0] * frame.shape[1]
        grass_area = 0
        
        if hasattr(results, 'masks') and results.masks is not None:
            for mask in results.masks.data:
                mask_np = mask.cpu().numpy()
                grass_area += np.sum(mask_np > 0.5)
        
        coverage_pct = (grass_area / frame_area) * 100
        
        needs_mowing = False
        if camera_id in self.mow_thresholds:
            needs_mowing = coverage_pct > self.mow_thresholds[camera_id]
        
        return {
            'camera_id': camera_id,
            'grass_coverage_pct': coverage_pct,
            'needs_mowing': needs_mowing,
            'timestamp': time.time()
        }
```

**Alternative Approach (No Training Required):**

```python
# grass_monitor_simple.py
import cv2
import numpy as np

class SimpleGrassMonitor:
    """Green coverage analysis without ML model"""
    
    def __init__(self):
        # HSV ranges for green grass
        self.green_lower = np.array([35, 40, 40])
        self.green_upper = np.array([85, 255, 255])
    
    def analyze_grass(self, frame: np.ndarray, camera_id: str) -> dict:
        """Analyze grass using color thresholding"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.green_lower, self.green_upper)
        
        # Calculate green coverage
        frame_area = frame.shape[0] * frame.shape[1]
        green_pixels = np.sum(mask > 0)
        coverage_pct = (green_pixels / frame_area) * 100
        
        # Texture analysis (grass = high frequency texture)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture_score = np.var(laplacian)
        
        # Needs mowing if: high green coverage + low texture (flat grass)
        needs_mowing = coverage_pct > 60 and texture_score < 500
        
        return {
            'camera_id': camera_id,
            'grass_coverage_pct': coverage_pct,
            'texture_score': texture_score,
            'needs_mowing': needs_mowing,
            'timestamp': time.time()
        }
```

### 4.3 Face Recognition - InsightFace with ArcFace

**Why InsightFace:**
- Highest accuracy (LFW: 99.86%)
- ArcFace model optimized for edge devices
- Better than DeepFace (99.65%) and FaceNet (99.63%)
- Active maintenance and TensorRT support

**Installation:**

```bash
source ~/cctv-ai/bin/activate
pip install insightface onnxruntime-gpu
```

**Face Recognition System:**

```python
# face_recognizer.py
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import sqlite3
import pickle
from typing import Optional, List
import time

class FaceRecognizer:
    def __init__(self, detection_size: int = 640):
        # Initialize InsightFace with GPU
        self.app = FaceAnalysis(
            providers=['CUDAExecutionProvider', 'CPUExecutionProvider'],
            allowed_modules=['detection', 'recognition']
        )
        self.app.prepare(ctx_id=0, det_size=(detection_size, detection_size))
        
        # SQLite database for face embeddings
        self.db_path = '/home/jetson/cctv-ai/face_database.db'
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for face storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                employee_id TEXT UNIQUE NOT NULL,
                embedding BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                face_id INTEGER,
                camera_id TEXT,
                confidence REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (face_id) REFERENCES faces(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_face(self, name: str, employee_id: str, face_image: np.ndarray) -> bool:
        """Register new face in database"""
        faces = self.app.get(face_image)
        
        if len(faces) == 0:
            return False
        
        # Use first detected face (ensure only one face in registration image)
        face = faces[0]
        embedding = face.embedding
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO faces (name, employee_id, embedding) VALUES (?, ?, ?)',
                (name, employee_id, pickle.dumps(embedding))
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def recognize_faces(self, frame: np.ndarray, camera_id: str, 
                       threshold: float = 0.6) -> List[dict]:
        """Detect and recognize faces in frame"""
        faces = self.app.get(frame)
        results = []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, employee_id, embedding FROM faces WHERE is_active=1')
        registered_faces = cursor.fetchall()
        conn.close()
        
        for face in faces:
            embedding = face.embedding
            bbox = face.bbox.astype(int)
            
            best_match = None
            best_similarity = 0
            
            for face_id, name, employee_id, stored_embedding in registered_faces:
                stored_emb = pickle.loads(stored_embedding)
                
                # Cosine similarity
                similarity = np.dot(embedding, stored_emb) / (
                    np.linalg.norm(embedding) * np.linalg.norm(stored_emb)
                )
                
                if similarity > best_similarity and similarity >= threshold:
                    best_similarity = similarity
                    best_match = {
                        'face_id': face_id,
                        'name': name,
                        'employee_id': employee_id
                    }
            
            result = {
                'bbox': bbox,
                'matched': best_match is not None,
                'name': best_match['name'] if best_match else 'Unknown',
                'employee_id': best_match['employee_id'] if best_match else None,
                'confidence': float(best_similarity),
                'camera_id': camera_id,
                'timestamp': time.time()
            }
            
            results.append(result)
            
            # Log access attempt
            if best_match:
                self.log_access(best_match['face_id'], camera_id, best_similarity)
        
        return results
    
    def log_access(self, face_id: int, camera_id: str, confidence: float):
        """Log face recognition event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO access_log (face_id, camera_id, confidence) VALUES (?, ?, ?)',
            (face_id, camera_id, confidence)
        )
        
        conn.commit()
        conn.close()
```

---

## 5. WHATSAPP ALERT INTEGRATION (STARSENDER)

### 5.1 Starsender API Setup

**Starsender Configuration:**
1. Register at: https://ardev.id/tool/starsender/
2. Create device in Starsender dashboard
3. Get API key from: Devices > Settings > API Key
4. Note device ID

### 5.2 WhatsApp Alert Manager

```python
# whatsapp_alert.py
import requests
import base64
import time
from typing import Optional

class WhatsAppAlerter:
    def __init__(self, api_key: str, device_id: str, base_url: str = 'https://waapi.tk'):
        self.api_key = api_key
        self.device_id = device_id
        self.base_url = base_url
        self.headers = {'apikey': api_key}
        
        # Rate limiting
        self.last_send_time = 0
        self.min_interval = 5  # seconds between alerts
    
    def send_text(self, phone_number: str, message: str) -> bool:
        """Send text message via Starsender"""
        # Rate limiting
        if time.time() - self.last_send_time < self.min_interval:
            time.sleep(self.min_interval - (time.time() - self.last_send_time))
        
        url = f'{self.base_url}/api/sendText'
        params = {
            'id_device': self.device_id,
            'tujuan': f'{phone_number}@s.whatsapp.net',
            'message': message
        }
        
        try:
            response = requests.post(url, headers=self.headers, params=params, timeout=10)
            self.last_send_time = time.time()
            return response.status_code == 200
        except Exception as e:
            print(f"WhatsApp send failed: {e}")
            return False
    
    def send_image(self, phone_number: str, message: str, image_path: str) -> bool:
        """Send image with caption via Starsender"""
        if time.time() - self.last_send_time < self.min_interval:
            time.sleep(self.min_interval - (time.time() - self.last_send_time))
        
        url = f'{self.base_url}/api/sendFiles'
        params = {
            'id_device': self.device_id,
            'tujuan': f'{phone_number}@s.whatsapp.net',
            'message': message
        }
        
        try:
            with open(image_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, headers=self.headers, params=params, files=files, timeout=10)
            self.last_send_time = time.time()
            return response.status_code == 200
        except Exception as e:
            print(f"WhatsApp image send failed: {e}")
            return False
    
    def send_image_url(self, phone_number: str, message: str, image_url: str) -> bool:
        """Send image from URL via Starsender"""
        if time.time() - self.last_send_time < self.min_interval:
            time.sleep(self.min_interval - (time.time() - self.last_send_time))
        
        url = f'{self.base_url}/api/sendFileUrl'
        params = {
            'id_device': self.device_id,
            'tujuan': f'{phone_number}@s.whatsapp.net',
            'message': message,
            'file_url': image_url
        }
        
        try:
            response = requests.post(url, headers=self.headers, params=params, timeout=10)
            self.last_send_time = time.time()
            return response.status_code == 200
        except Exception as e:
            print(f"WhatsApp URL send failed: {e}")
            return False
```

### 5.3 Alert Templates

```python
# alert_templates.py
from datetime import datetime

class AlertTemplates:
    @staticmethod
    def intrusion_alert(camera_name: str, location: str, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp)
        return (
            f"🚨 *INTRUSION DETECTED*\n\n"
            f"📍 Camera: {camera_name}\n"
            f"🏢 Location: {location}\n"
            f"⏰ Time: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"⚠️ Unauthorized person in restricted zone!"
        )
    
    @staticmethod
    def grass_alert(camera_name: str, location: str, coverage: float) -> str:
        return (
            f"🌱 *GRASS MAINTENANCE REQUIRED*\n\n"
            f"📍 Camera: {camera_name}\n"
            f"🏢 Location: {location}\n"
            f"📊 Grass Coverage: {coverage:.1f}%\n\n"
            f"✂️ Grass needs mowing!"
        )
    
    @staticmethod
    def face_recognition_alert(name: str, camera_name: str, 
                               confidence: float, is_authorized: bool) -> str:
        status = "✅ AUTHORIZED" if is_authorized else "⚠️ UNAUTHORIZED"
        return (
            f"👤 *FACE RECOGNITION ALERT*\n\n"
            f"{status}\n"
            f"📛 Name: {name}\n"
            f"📍 Camera: {camera_name}\n"
            f"🎯 Confidence: {confidence:.2%}\n"
            f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
    
    @staticmethod
    def system_alert(message: str) -> str:
        return f"⚙️ *SYSTEM ALERT*\n\n{message}"
```

---

## 6. MAIN INTEGRATION SYSTEM

### 6.1 Multi-Stream Processor

```python
# main.py
import cv2
import threading
import time
import sqlite3
from typing import Dict, List
import numpy as np

from rtsp_manager import RTSPManager
from intrusion_detector import IntrusionDetector
from grass_monitor import SimpleGrassMonitor
from face_recognizer import FaceRecognizer
from whatsapp_alert import WhatsAppAlerter
from alert_templates import AlertTemplates

class CCTVSystem:
    def __init__(self, config: dict):
        self.config = config
        
        # Initialize components
        self.rtsp_manager = RTSPManager()
        self.intrusion_detector = IntrusionDetector(
            model_path=config['intrusion_model'],
            confidence=0.5
        )
        self.grass_monitor = SimpleGrassMonitor()
        self.face_recognizer = FaceRecognizer()
        self.whatsapp = WhatsAppAlerter(
            api_key=config['starsender_api_key'],
            device_id=config['starsender_device_id']
        )
        
        # Alert throttling (prevent spam)
        self.last_alert: Dict[str, float] = {}
        self.alert_cooldown = {
            'intrusion': 300,  # 5 minutes
            'grass': 86400,    # 24 hours
            'face': 60         # 1 minute
        }
        
        # Camera configuration
        self.cameras = config['cameras']
        self.alert_phones = config['alert_phones']
        
        # Processing threads
        self.running = False
        self.threads: List[threading.Thread] = []
    
    def setup_cameras(self):
        """Initialize all camera streams"""
        for cam_id, cam_config in self.cameras.items():
            success = self.rtsp_manager.add_stream(
                stream_id=cam_id,
                rtsp_url=cam_config['rtsp_url']
            )
            
            if success:
                # Set restricted zone for intrusion detection
                if 'restricted_zone' in cam_config:
                    self.intrusion_detector.set_restricted_zone(
                        cam_id, 
                        cam_config['restricted_zone']
                    )
                
                # Set grass threshold
                if 'grass_threshold' in cam_config:
                    self.grass_monitor.set_mow_threshold(
                        cam_id,
                        cam_config['grass_threshold']
                    )
                
                print(f"✅ Camera {cam_id} initialized")
            else:
                print(f"❌ Camera {cam_id} failed to initialize")
    
    def can_send_alert(self, alert_type: str, camera_id: str) -> bool:
        """Check if alert can be sent (rate limiting)"""
        key = f"{alert_type}_{camera_id}"
        now = time.time()
        
        if key not in self.last_alert:
            return True
        
        cooldown = self.alert_cooldown.get(alert_type, 300)
        return (now - self.last_alert[key]) > cooldown
    
    def send_alert(self, alert_type: str, camera_id: str, message: str, 
                   image_path: Optional[str] = None):
        """Send WhatsApp alert with rate limiting"""
        if not self.can_send_alert(alert_type, camera_id):
            return
        
        for phone in self.alert_phones:
            if image_path:
                self.whatsapp.send_image(phone, message, image_path)
            else:
                self.whatsapp.send_text(phone, message)
        
        self.last_alert[f"{alert_type}_{camera_id}"] = time.time()
        print(f"📱 Alert sent: {alert_type} for {camera_id}")
    
    def process_camera(self, camera_id: str):
        """Process single camera stream"""
        cam_config = self.cameras[camera_id]
        frame_count = 0
        
        while self.running:
            frame = self.rtsp_manager.get_frame(camera_id)
            
            if frame is None:
                time.sleep(1)
                continue
            
            # Process every Nth frame (reduce load)
            process_interval = cam_config.get('process_interval', 30)
            if frame_count % process_interval != 0:
                frame_count += 1
                continue
            
            timestamp = time.time()
            
            # 1. Intrusion Detection
            intrusions = self.intrusion_detector.detect_intrusion(frame, camera_id)
            if intrusions:
                alert_msg = AlertTemplates.intrusion_alert(
                    camera_name=cam_config['name'],
                    location=cam_config['location'],
                    timestamp=timestamp
                )
                
                # Save frame with bounding boxes
                alert_frame = frame.copy()
                for intrusion in intrusions:
                    x1, y1, x2, y2 = map(int, intrusion['bbox'])
                    cv2.rectangle(alert_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                
                alert_path = f'/tmp/alert_{camera_id}_{int(timestamp)}.jpg'
                cv2.imwrite(alert_path, alert_frame)
                
                self.send_alert('intrusion', camera_id, alert_msg, alert_path)
            
            # 2. Grass Monitoring (once per hour)
            if frame_count % (process_interval * 120) == 0:  # ~1 hour at 30fps
                grass_result = self.grass_monitor.analyze_grass(frame, camera_id)
                if grass_result['needs_mowing']:
                    alert_msg = AlertTemplates.grass_alert(
                        camera_name=cam_config['name'],
                        location=cam_config['location'],
                        coverage=grass_result['grass_coverage_pct']
                    )
                    self.send_alert('grass', camera_id, alert_msg)
            
            # 3. Face Recognition
            faces = self.face_recognizer.recognize_faces(frame, camera_id)
            for face in faces:
                if not face['matched']:  # Unknown face
                    alert_msg = AlertTemplates.face_recognition_alert(
                        name=face['name'],
                        camera_name=cam_config['name'],
                        confidence=face['confidence'],
                        is_authorized=False
                    )
                    self.send_alert('face', camera_id, alert_msg)
            
            frame_count += 1
    
    def start(self):
        """Start all processing threads"""
        self.running = True
        self.setup_cameras()
        
        # Start thread per camera
        for camera_id in self.cameras.keys():
            thread = threading.Thread(
                target=self.process_camera,
                args=(camera_id,),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
        
        print(f"🎥 System started with {len(self.cameras)} cameras")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop all processing"""
        print("Stopping system...")
        self.running = False
        
        for thread in self.threads:
            thread.join(timeout=5)
        
        self.rtsp_manager.cleanup()
        print("System stopped")


# Configuration
CONFIG = {
    'intrusion_model': '/home/jetson/cctv-ai/yolo11n.engine',
    'starsender_api_key': 'YOUR_API_KEY',
    'starsender_device_id': 'YOUR_DEVICE_ID',
    'alert_phones': ['6281234567890', '6281234567891'],  # Indonesian format
    
    'cameras': {
        'cam1': {
            'name': 'Gate Entrance',
            'location': 'Site A - Main Gate',
            'rtsp_url': 'rtsp://admin:password@192.168.1.10:554/unicast/c1/s1/live',
            'process_interval': 30,  # Process every 30 frames
            'restricted_zone': [(100, 200), (300, 200), (300, 400), (100, 400)],
            'grass_threshold': 70
        },
        'cam2': {
            'name': 'Parking Lot',
            'location': 'Site A - Parking',
            'rtsp_url': 'rtsp://admin:password@192.168.1.11:554/unicast/c1/s1/live',
            'process_interval': 30,
            'restricted_zone': [(150, 250), (350, 250), (350, 450), (150, 450)],
            'grass_threshold': 65
        },
        'cam3': {
            'name': 'Building Entrance',
            'location': 'Site A - Building',
            'rtsp_url': 'rtsp://admin:password@192.168.1.12:554/unicast/c1/s1/live',
            'process_interval': 15,  # Higher frequency for face recognition
            'grass_threshold': 60
        },
        'cam4': {
            'name': 'Perimeter',
            'location': 'Site A - Back Fence',
            'rtsp_url': 'rtsp://admin:password@192.168.1.13:554/unicast/c1/s1/live',
            'process_interval': 30,
            'restricted_zone': [(50, 300), (590, 300), (590, 480), (50, 480)],
            'grass_threshold': 75
        }
    }
}

if __name__ == '__main__':
    system = CCTVSystem(CONFIG)
    system.start()
```

---

## 7. SYSTEMD SERVICE (Auto-start on Boot)

```bash
# Create service file
sudo nano /etc/systemd/system/cctv-ai.service
```

```ini
[Unit]
Description=CCTV AI Processing System
After=network.target

[Service]
Type=simple
User=jetson
WorkingDirectory=/home/jetson/cctv-ai
Environment="PATH=/home/jetson/cctv-ai/bin"
ExecStart=/home/jetson/cctv-ai/bin/python /home/jetson/cctv-ai/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable cctv-ai
sudo systemctl start cctv-ai

# Check status
sudo systemctl status cctv-ai

# View logs
sudo journalctl -u cctv-ai -f
```

---

## 8. PERFORMANCE BENCHMARKS

### Expected Performance (Jetson Orin Nano 8GB)

| Configuration | Streams | FPS/Stream | Total FPS | GPU Util | Latency |
|--------------|---------|------------|-----------|----------|---------|
| YOLOv11n only | 4 | 25-30 | 100-120 | 60-70% | 50-80ms |
| YOLOv11n + Face | 4 | 15-20 | 60-80 | 80-90% | 100-150ms |
| YOLOv11n + Face + Grass | 4 | 10-15 | 40-60 | 90-95% | 150-200ms |
| All features | 6 | 8-10 | 48-60 | 95-100% | 200-300ms |

### Optimization Tips

```bash
# 1. Use sub-stream (lower resolution) for AI processing
# Main stream: 1920×1080 → Sub-stream: 640×480

# 2. Enable Jetson power modes
sudo nvpmodel -m 0  # MAXN (max performance)
sudo jetson_clocks  # Max clocks (increases heat)

# 3. Monitor GPU usage
tegrastats  # Real-time system stats
jtop        # Install: pip3 install -U jetson-stats

# 4. TensorRT optimization flags
# Already included in export: half=True, optimize=True

# 5. Reduce process interval for non-critical cameras
# Grass monitoring: every 1 hour instead of every frame
```

---

## 9. FACE DATABASE MANAGEMENT

### Register Faces (Command Line)

```python
# register_faces.py
import cv2
from face_recognizer import FaceRecognizer

recognizer = FaceRecognizer()

# Capture from webcam or load image
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

# Register face
success = recognizer.register_face(
    name="John Doe",
    employee_id="EMP001",
    face_image=frame
)

if success:
    print("✅ Face registered successfully")
else:
    print("❌ Registration failed (face not detected or duplicate ID)")
```

### Query Database

```bash
# View registered faces
sqlite3 /home/jetson/cctv-ai/face_database.db "SELECT id, name, employee_id, created_at FROM faces;"

# View access logs
sqlite3 /home/jetson/cctv-ai/face_database.db "SELECT * FROM access_log ORDER BY timestamp DESC LIMIT 50;"

# Deactivate face (revoke access)
sqlite3 /home/jetson/cctv-ai/face_database.db "UPDATE faces SET is_active=0 WHERE employee_id='EMP001';"
```

---

## 10. TROUBLESHOOTING

### Common Issues

**RTSP Connection Failures:**
```bash
# Test connectivity
ping <camera-ip>

# Check RTSP port
nc -zv <camera-ip> 554

# Verify credentials in VLC first
vlc rtsp://admin:password@<camera-ip>:554/unicast/c1/s1/live
```

**TensorRT Model Loading Errors:**
```bash
# Check CUDA version compatibility
nvcc --version

# Re-export model with correct settings
python3 export_model.py

# Verify .engine file exists
ls -lh /home/jetson/cctv-ai/*.engine
```

**Out of Memory (OOM):**
```bash
# Monitor memory
tegrastats

# Reduce batch size or model size
# Switch from YOLOv11n to YOLOv11n (already smallest)
# Reduce image size: imgsz=416 instead of 640
```

**WhatsApp Alerts Not Sending:**
```bash
# Test API manually
curl -X POST "https://waapi.tk/api/sendText?id_device=YOUR_ID&tujuan=6281234567890@s.whatsapp.net&message=Test" \
  -H "apikey: YOUR_API_KEY"

# Check device status in Starsender dashboard
# Ensure phone number format: 628xxxxxxxxxx (no + or 0 prefix)
```

**High CPU Usage:**
```bash
# Ensure GPU is being used
python3 -c "import torch; print(torch.cuda.is_available())"

# Check if OpenCV is using CUDA
python3 -c "import cv2; print(cv2.getBuildInformation())"

# Reduce number of simultaneous streams or FPS
```

---

## 11. COST BREAKDOWN

### Per Site (4 Cameras)

| Item | Unit Cost | Qty | Total |
|------|-----------|-----|-------|
| Jetson Orin Nano Super 8GB | $249 | 1 | $249 |
| MicroSD Card 128GB | $25 | 1 | $25 |
| Power Supply 5V/4A | $15 | 1 | $15 |
| Ethernet Cable | $5 | 1 | $5 |
| Enclosure | $20 | 1 | $20 |
| **Total per site** | | | **$314** |

### Total Project (10 Sites)

| Item | Total |
|------|-------|
| Hardware (10× Jetson kits) | $3,140 |
| Starsender API (monthly) | ~$50-100 |
| Development time | 2-3 weeks |
| Deployment time | 1 week |
| **Total estimated** | **$3,500-4,000** |

---

## 12. TIMELINE

| Phase | Duration | Tasks |
|-------|----------|-------|
| Setup & Testing | 3-4 days | Jetson flash, RTSP testing, model export |
| Development | 7-10 days | Integration code, face database, alerts |
| Grass Model Training | 3-5 days | Data collection, labeling, training |
| On-site Deployment | 5-7 days | 10 sites installation, calibration |
| Testing & Tuning | 3-5 days | Performance optimization, threshold tuning |
| **Total** | **3-4 weeks** | |

---

## 13. FILES TO CREATE

```
/home/jetson/cctv-ai/
├── main.py                 # Main system orchestrator
├── rtsp_manager.py         # RTSP stream management
├── intrusion_detector.py   # YOLOv11 intrusion detection
├── grass_monitor.py        # Grass monitoring (simple or ML)
├── face_recognizer.py      # InsightFace recognition
├── whatsapp_alert.py       # Starsender integration
├── alert_templates.py      # WhatsApp message templates
├── export_model.py         # TensorRT model export
├── register_faces.py       # Face registration utility
├── config.json             # Configuration file
├── face_database.db        # SQLite face database
├── yolo11n.engine          # TensorRT intrusion model
├── grass_v1.engine         # TensorRT grass model (if using ML)
└── requirements.txt        # Python dependencies
```

### requirements.txt
```
ultralytics>=8.3.0
insightface>=0.7.3
onnxruntime-gpu>=1.18.0
opencv-python>=4.10.0
numpy>=1.26.0
requests>=2.32.0
shapely>=2.0.0
sqlite3
```

---

## 14. SECURITY CONSIDERATIONS

1. **Change default passwords** on all Uniview cameras/NVR
2. **Isolate CCTV network** from main corporate network (VLAN)
3. **Enable RTSP authentication** (Digest mode)
4. **Encrypt face database** (SQLite encryption extension)
5. **Rate limit WhatsApp alerts** (prevent abuse)
6. **Regular backups** of face database
7. **Audit logs** for all access events
8. **Physical security** for Jetson devices (locked enclosure)

---

## 15. NEXT STEPS

1. **Order hardware**: 10× Jetson Orin Nano Super + accessories
2. **Setup test environment**: 1 Jetson + 1-2 cameras for development
3. **Collect grass images**: Across all 10 sites, different conditions
4. **Register employee faces**: Start with security team, expand gradually
5. **Configure Starsender**: Test WhatsApp alerts with test numbers
6. **Deploy pilot**: 1 site full deployment, validate performance
7. **Scale**: Roll out to remaining 9 sites

---

**Contact for Support:**
- NVIDIA Jetson Forums: https://forums.developer.nvidia.com/
- Ultralytics YOLO Docs: https://docs.ultralytics.com/
- InsightFace Docs: https://insightface.ai/
- Starsender API: https://documenter.getpostman.com/view/13688543/TVzPkxtt
