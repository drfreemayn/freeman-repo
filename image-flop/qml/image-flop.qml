import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.2

import freeman 1.0

ApplicationWindow {
    id: appWindow
    title: "Image-flop"
    height: 500
    width: 800
    visible: true

    signal loadImageChosen(url path)
    signal saveImageChosen(url path)

    FileDialog {
        id: loadImageDialog
        title: "Open file"
        folder: shortcuts.home
        nameFilters: ["Image files (*.jpg *.png)"]
        onAccepted: {
            appWindow.loadImageChosen(loadImageDialog.fileUrl);
        }
    }

    FileDialog {
        id: saveImageDialog
        title: "Save file"
        folder: shortcuts.home
        selectExisting: false
        nameFilters: ["Image files (*.jpg *.png)"]
        onAccepted: {
            appWindow.saveImageChosen(saveImageDialog.fileUrl);
        }
    }

    FilterDialog {
        id: applyGlobalFilterDialog
    }

    menuBar: MainMenuBar {}

    MainContent {
        id: mainContent
    }
}