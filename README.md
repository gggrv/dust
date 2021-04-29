# dust

Tray application that can do anything. All functions are defined as plugins (stylistically named "pieces") that are independent of each other and may be enabled or disabled at any time. All loaded plugins may access each other's data. Work in progress.

## Available plugins

| Item | Category | Aim | Scenario | What it does | State | Tool |
| :------------ | :------------ | :- | :- | :- | :- | :- |
| emptiness | cosmetics | Temporary solution to information overload | Computer with multiple monitors | Obscures contents of the monitors that the mouse pointer is not present on with neutral grey screensaver | Good | PyQt5 |
| grimoire | utility | Extended context menu for any program | Abundancy of small simple routines that require a lot of switching between different programs | Follows mouse pointer in undistracting manner, accepts drag&drop input, expands upon interaction | Naked | PyQt5 |
| ribbon | utility | Simple tool to help recognise complex patterns and dependencies | Need to establish a routine, change a habit, track something | Manages innumerous amount of simple uniform .csv files in human-friendly manner | Work in progress | pandas, PyQt5 |
