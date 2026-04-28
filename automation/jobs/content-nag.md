Run the content accountability check for today's publishing habit.

You will receive a scheduler header like `[SCHEDULED JOB: ...]`.
Use it to set tone:
- morning = light nudge
- midday = firmer push
- final = hard push; optimize for shipping something small today

Rules:
- Post to `content`.
- Keep it short and direct.
- Push action, not reflection.
- Do not give a long pep talk.
- If there is no proof in thread that something is already published today, assume it is not posted yet.
- Prefer the smallest publishable unit over ambitious ideas.
- Optimize for these channels only:
  - `Threads`
  - `LinkedIn`
  - `Instagram Carousel`
- Channel priority:
  - first: `Threads`
  - second: `LinkedIn`
  - third: `Instagram Carousel`
- If unsure, default to `Threads` text post.

Output format:
- Status: one short line
- Best channel: one short line
- Fastest publishable option: one short line
- Next action: one concrete command

Escalation logic:
- Morning: suggest the easiest valid post for today.
- Midday: call out drift and shrink the scope.
- Final: remove all optionality and force the smallest shippable post.

Good examples of smallest publishable unit:
- one `Threads` text post
- one `LinkedIn` text post
- one `Instagram Carousel` outline with 5 slides
- one voice note turned into a `Threads` draft
