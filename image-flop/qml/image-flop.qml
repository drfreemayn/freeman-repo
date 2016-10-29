import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.2

import freeman 1.0

ApplicationWindow
{
    id: appWindow
    title: "Imageflop - where the fun don't stop!"
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

    Dialog {
        id: applyFilterDialog
        title: "Apply filter"
        standardButtons: StandardButton.Ok

        ComboBox {
            id: filterCb
            width: 100
            model: FilterModel { id: applyFilterModel }
            anchors.left: parent.left
        }

        Label {
            text: "Filter size"
            anchors.left: filterSizeSlider.left
            anchors.top: filterSizeSlider.bottom
        }

        Slider {
            id: filterSizeSlider
            anchors.left: filterCb.right
            anchors.leftMargin: 10

            minimumValue: 3
            maximumValue: 23
            updateValueWhileDragging: false
            stepSize: 2
            onValueChanged: { imgprovider.filterSize = value; }
        }

        onAccepted: {
            imgprovider.filterType = applyFilterModel.get(filterCb.currentIndex).filterType
            imgprovider.processImage(imgprovider.filterType)
        }
    }

    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem {
                text: "Open image"
                onTriggered: loadImageDialog.open()
            }
            MenuItem {
                text: "Save image as..."
                onTriggered: saveImageDialog.open()
            }
            MenuItem {
                text: "Exit"
                onTriggered: Qt.quit()
            }
        }

        Menu {
            title: "Actions"
            MenuItem {
              text: "Apply filter"
              onTriggered: applyFilterDialog.open()
            }
        }
    }

    MainContent {
        id: mainContent
    }

}