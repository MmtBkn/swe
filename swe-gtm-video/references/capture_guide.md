# Browser and Device Capture Guide

## Goal

Capture the feature as it truly works, in a controlled and beautiful state.

## Setup

- Use a test tenant or seeded environment.
- Remove PII and confidential data.
- Disable unstable UI noise such as random banners, timestamps, or unrelated notifications.
- Set browser viewport to the target export ratio.
- Prepare a capture script with exact user actions.

## Capture passes

Capture multiple passes instead of trying to get one perfect take:

1. Hero flow: full feature path.
2. Detail pass: key UI elements.
3. Before state: pain/workaround.
4. After state: success/outcome.
5. Still frames: clean frames for Veo/image-to-video or thumbnails.

## Retake triggers

- PII or internal data appears.
- UI is too small to read.
- Cursor movement distracts.
- The flow fails or loads slowly in a way not intended for the story.
- Branding is incorrect.
- Generated or captured footage implies unsupported behavior.
