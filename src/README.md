## Downloading the Data

Since the data is hosted on Kaggle.com, it is necessary for you to complete the following steps **before executing any of the scripts:**

1. #### [Authentication](https://www.kaggle.com/docs/api)

   In order to use the [Kaggle’s public API](https://github.com/Kaggle/kaggle-api#api-credentials), you must first authenticate using an API token. From the site header, click on your user profile picture, then on “My Account” from the dropdown menu. This will take you to your account settings at [https://www.kaggle.com/account](https://www.kaggle.com/). Scroll down to the section of the page labelled API:

   To create a new token, click on the “Create New API Token” button. This will download a fresh authentication token onto your machine.

   If you are using the Kaggle CLI tool, the tool will look for this token at ~/.kaggle/kaggle.json on Linux, OSX, and other UNIX-based operating systems, and at C:\Users<Windows-username>.kaggle\kaggle.json on Windows. If the token is not there, an error will be raised. Hence, once you’ve downloaded the token, you should move it from your Downloads folder to this folder.

   If you are using the Kaggle API directly, where you keep the token doesn’t matter, so long as you are able to provide your credentials at runtime.

2. #### **From your Terminal**

   * Create a hidden folder in your home directory `.kaggle/`

     ```
     $ mkdir ~/.kaggle/
     ```

   * Move your `kaggle.json` file that was automatically downloaded to your default download directory to the newly created `.kaggle/` file folder on your system

     ```
     $ mv kaggle.json ~/.kaggle/
     ```

   * Change directories to your hidden folder `.kaggle/` and change the permissioning on your `kaggle.json` file:

     ```
     $ cd ~/.kaggle/
     $ chmod 600 kaggle.json
     ```

   

## Download this Repository & Create a Virtual Environment
