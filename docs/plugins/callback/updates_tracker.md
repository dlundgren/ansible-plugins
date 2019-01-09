# Plugin :: callback :: updates_tracker

This callback is designed to let you know whether `system updated` or `system rebooted` notifications are called.

At the end of the play it will output something similar to the following:

- `Updated : host01`
- `Updated / Rebooted : host02`
- `No systems updated or rebooted`

# Usage

You need to set the `use_updates_tracker = yes` as a var otherwise it won't track

