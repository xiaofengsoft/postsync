// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
const { contextBridge, ipcRenderer } = require('electron/renderer')

contextBridge.exposeInMainWorld('electronAPI', {
  windowMaximize: () => ipcRenderer.send('window-max'),
  windowMinimize: () => ipcRenderer.send('window-min'),
  windowClose: () => ipcRenderer.send('window-close'),
  getImageDataUrl: (imagePath) => ipcRenderer.invoke('get-image-data-url', imagePath)
})