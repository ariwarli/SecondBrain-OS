import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

INPUT_HTML = Path("/Users/banirisset/banirisset/personal-brand/threads/carousels/2026-03-27-mac-shortcuts-v2.html")
OUTPUT_DIR = Path("/Users/banirisset/banirisset/personal-brand/threads/carousels/slides-v2")
OUTPUT_DIR.mkdir(exist_ok=True)

TOTAL_SLIDES = 7
VIEW_W, VIEW_H = 420, 525
SCALE = 1080 / 420

async def export_slides():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
        )
        ctx = await browser.new_context(
            viewport={"width": VIEW_W, "height": VIEW_H},
            device_scale_factor=SCALE,
        )
        page = await ctx.new_page()
        await page.set_content(
            INPUT_HTML.read_text(encoding="utf-8"),
            wait_until="networkidle"
        )
        await page.wait_for_timeout(4000)

        await page.evaluate("""() => {
            document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption')
                .forEach(el => el.style.display='none');
            document.querySelector('.ig-frame').style.cssText =
                'width:420px;height:525px;max-width:none;border-radius:0;box-shadow:none;overflow:hidden;margin:0;padding:0;';
            document.querySelector('.carousel-viewport').style.cssText =
                'width:420px;height:525px;aspect-ratio:unset;overflow:hidden;cursor:default;';
            document.body.style.cssText =
                'padding:0;margin:0;display:block;overflow:hidden;background:transparent;';
        }""")
        await page.wait_for_timeout(500)

        for i in range(TOTAL_SLIDES):
            await page.evaluate(
                f"document.querySelector('.carousel-track').style.transition='none';"
                f"document.querySelector('.carousel-track').style.transform='translateX({-i * 420}px)';"
            )
            await page.wait_for_timeout(500)
            out_path = OUTPUT_DIR / f"slide_{i+1:02d}.png"
            await page.screenshot(
                path=str(out_path),
                clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H}
            )
            print(f"✓ slide {i+1}/{TOTAL_SLIDES} → {out_path.name}")

        await ctx.close()
        await browser.close()
        print(f"\nDone. {TOTAL_SLIDES} slides saved to:\n{OUTPUT_DIR}")

asyncio.run(export_slides())
