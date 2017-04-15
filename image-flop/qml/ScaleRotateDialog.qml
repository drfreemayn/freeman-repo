import QtQuick.Dialogs 1.2
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3
import QtQuick 2.7

Dialog {
    title: "Scaling and rotation"
    standardButtons: StandardButton.Ok

    ColumnLayout {
        id: dialogLayout
        anchors.fill: parent

        RowLayout {
            id: scalingLayout
            spacing: 5    

            Label {
                id: scalingLabel
                text: "Scaling"
            }
            Label {
                id: scalingXLabel
                text: "x: "
            }
            TextField {
                id: scalingXInput
                placeholderText: "1,0"
                text: "1,0"
                validator: DoubleValidator{ bottom: 0 }
                horizontalAlignment: TextField.AlignHCenter
                inputMethodHints: Qt.ImhFormattedNumbersOnly 
                maximumLength: 5
            }
            Label {
                 id: scalingYLabel
                 text: "y: "
            }
            TextField {
                id: scalingYInput
                placeholderText: "1,0"
                text: "1,0"
                validator: DoubleValidator{ bottom: 0 }
                horizontalAlignment: TextField.AlignHCenter
                inputMethodHints: Qt.ImhFormattedNumbersOnly
                maximumLength: 5
            }
        }

        RowLayout {
            id: rotationLayout
            spacing: 5      

            Label {
                id: rotationLabel
                text: "Clockwise rotation (deg):"
            }
            TextField {
                id: rotationInput
                placeholderText: "0"
                text: "0"
                validator: DoubleValidator {}
                horizontalAlignment: TextField.AlignHCenter
                inputMethodHints: Qt.ImhFormattedNumbersOnly
                maximumLength: 5
            }
        }
    }

    onAccepted: {
        var sx = parseFloat(scalingXInput.text.replace(",", "."))
        var sy = parseFloat(scalingYInput.text.replace(",", "."))
        var ang = parseFloat(rotationInput.text.replace(",", "."))
        imgprovider.scaleAndRotate(sx, sy, ang)
        scalingXInput.text = "1,0"
        scalingYInput.text = "1,0"
        rotationInput.text = "0"
    }
}
