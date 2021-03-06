==============================
Firefox OS Certification Tests
==============================

Tests to verify the functionality and characteristics of Firefox OS
devices, including a test harness that allows a human to dynamically
add input whilst running the tests.

The test suite is designed to run on unprivileged devices and does not
rely on high level instrumentation.  Instead human interaction is
needed throughout the test suite to perform various instructions in
order to assert that conditions are met on the device.

Running the test suite will open a tab in your web browser that will
show the progress of test suite as it's running and occasionally ask
you to interact with the device in certain ways.  The tests will then
assert that the expectations are met.

Requirements
============

The certification test suite is intended to run on a host computer
attached to the device via USB cable.  Currently the host requires the
Linux or Mac OS operating systems with *adb* (Android Debug Bridge)
installed.

If you need to install adb, see
https://developer.mozilla.org/en-US/Firefox_OS/Debugging/Installing_ADB.

Once installed, add adb to your PATH in your *~/.bashrc* or equivalent
file, by adding the following line to the file (replacing $SDK_HOME
with the location of the Android SDK)::

    PATH=$SDK_HOME:$PATH

The device and the host machine running the tests must also be on the
same Wi-Fi network.

Enabling ADB
------------

Furthermore, you must turn on adb access on the device:

**For Firefox OS version 1.3:** Launch *Settings*, and navigate to
*Device Information* → *More Information* → *Developer*, then check
*Remote Debugging*.

**For version 1.4:** Launch *Settings*, and navigate to *Device
Information* → *More Information*, then check *Developer Options*.
Next, hold down the *Home* button, and close the *Settings* app (press
the x).  Finally, launch *Settings* again, and navigate to
*Developer*, then select *ADB only* in *Remote Debugging*.

Once this is done, go to Settings → Display and set the *Screen
Timeout* to *Never*. You need this because adb is will be disabled
when the device is locked.

Environment Setup
=================

Before running the test you need to set up a test environment.  This
involves setting up a Python virtual environment and installing the
right dependencies, and installing a test application on the remote
device.

This can be done automatically by invoking::

    source setup_environment.sh

Running Tests
=============

Execute ``python semiauto/environment.py`` to start an HTTP server on
port 6666.  In your browser, navigate to http://localhost:6666/ to
start the test run.
