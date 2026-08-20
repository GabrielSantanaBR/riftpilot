const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("riftpilot", {
  platform: process.platform,
  version: "0.4.0",
});
