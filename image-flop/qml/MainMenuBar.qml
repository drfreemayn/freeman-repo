
import QtQml 2.2
import QtQuick.Controls 1.4

MenuBar {

    Menu {
        title: "File"
        MenuItem {
            text: "Open image"
            onTriggered: loadImageDialog.open()
            shortcut: "Ctrl+O"
        }
        MenuItem {
            text: "Save image as..."
            onTriggered: saveImageDialog.open()
            shortcut: "Ctrl+S"
        }
        MenuItem {
            text: "Exit"
            onTriggered: Qt.quit()
            shortcut: "Alt+F4"
        }
    }

    Menu {
        title: "Actions"

        Connections {
            target: imgprovider
            onImageChanged: { 
                undoMenuItem.enabled = imgprovider.imageIdx < imgprovider.getNumImages()-1;
                redoMenuItem.enabled = imgprovider.imageIdx > 0;
            }
        }

        MenuItem {
          id: undoMenuItem
          text: "Undo"
          onTriggered: imgprovider.undoImage()
          shortcut: "Ctrl+Z"
          enabled: false
        }
        MenuItem {
          id: redoMenuItem
          text: "Redo"
          onTriggered: imgprovider.redoImage()
          shortcut: "Ctrl+Y"
          enabled: false
        }
        MenuItem {
          text: "Apply global filter"
          onTriggered: applyGlobalFilterDialog.open()
          shortcut: "Ctrl+F"
        }
    }
}