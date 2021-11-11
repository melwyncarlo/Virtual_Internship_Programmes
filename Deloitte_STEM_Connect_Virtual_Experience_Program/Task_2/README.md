## Task #2 : Data Analysis

<hr>

**Task description:** 
Build a dashboard to explore the client's telemetry data.

Because the [Tableau software](https://www.tableau.com/) does not exist for the Linux (Ubuntu) operating system, and the Windows version does not start using the [Wine software](https://www.winehq.org/), I relied on the Online Tableau version instead.

There is a caveat, however: it cannot upload the **61.3MB JSON** file (or any JSON file for that matter). So, I thought out of the box, and created a **Python** program (see **main.py**) to extract the required information in the form of a **CSV** file, and then uploaded that file onto the Online Tableau web-app, which it fortunately worked very well.

From there on, it was all about following the task resource PDF and downloading the generated bar graphs.

