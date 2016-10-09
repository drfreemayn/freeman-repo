import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.0

import freeman 1.0

ApplicationWindow 
{
    id: appWindow
    title: "Eye processing"
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
	}

	MainContent {
		id: mainContent
	}

}