import QtQuick.Dialogs 1.2
import QtQuick.Controls 1.4

Dialog {
    title: "Apply global filter"
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
        imgprovider.processImage(imgprovider.filterType, true)
    }
}
