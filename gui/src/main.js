const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const path = require('node:path');

require('@electron/remote/main').initialize();
// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

//控制台快捷键
app.on('ready', async () => {
  globalShortcut.register('CommandOrControl+Shift+i', function () {
    win.webContents.openDevTools()
  })
  createWindow();
})


const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    icon: 'assets/imgs/logo.png',
    width: 800,
    height: 600,
    autoHideMenuBar: true, // Hide the menu bar
    frame: false, // Remove the window frame
    useContentSize: true, // Use content size instead of window size
    transparent: false, // Make the window transparent
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true, // Allow node integration in the renderer process
      contextIsolation: true, // Enable context isolation
      enableRemoteModule: true, // Allow remote module in the renderer process
    },
  });

  //登录窗口最小化 
  ipcMain.on('window-min', function () {
    mainWindow.minimize();
  })
  //登录窗口最大化 
  ipcMain.on('window-max', function () {
    if (mainWindow.isMaximized()) {
      mainWindow.restore();
    } else {
      mainWindow.maximize();
    }
  })
  //登录窗口关闭
  ipcMain.on('window-close', function () {
    mainWindow.close();
  })
  // and load the index.html of the app.
  if (MAIN_WINDOW_VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(MAIN_WINDOW_VITE_DEV_SERVER_URL);
  } else {
    mainWindow.loadFile(path.join(__dirname, `../renderer/${MAIN_WINDOW_VITE_NAME}/index.html`));
  }

  // Open the DevTools.
  mainWindow.webContents.openDevTools();
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  // 获取图片的 base64 数据
  ipcMain.handle('get-image-data-url', async (event, imagePath) => {
    try {
      const fullPath = imagePath;
      const extname = path.extname(fullPath).toLowerCase();
      let mimeType;

      switch (extname) {
        case '.png':
          mimeType = 'image/png';
          break;
        case '.jpg':
        case '.jpeg':
          mimeType = 'image/jpeg';
          break;
        // ... 可以继续添加其他类型的图片
        default:
          throw new Error('不支持的文件类型');
      }
      const data = await fs.promises.readFile(fullPath);
      const base64Image = data.toString('base64');
      return `data:${mimeType};base64,${base64Image}`;
    } catch (error) {
      console.error('读取或处理文件时发生错误:', error);
      return '读取或处理文件时发生错误';
    }
  });
  createWindow();
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.
