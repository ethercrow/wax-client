import QtQuick 1.0

Rectangle {
    id: main
    width: 1024
    height: 600

    Row {

        anchors.fill: parent

        ListView {
            id: propertyListView
            objectName: "propertyListView"

            width: 150

            delegate: Item {
                Row {
                    Text {
                        text: key
                    }
                    Text {
                        text: value
                    }
                }
            }

            model: currentPropertiesModel // updated from python

            anchors.top: parent.top
            anchors.bottom: parent.bottom
        }

        ListView {
            id: hierarchyView
            objectName: "hierarchyView"

            width: parent.width - propertyListView.width - canvas.width

            delegate: Text {
                text: display
            }

            model: treeModel // updated from python

            anchors.top: parent.top
            anchors.bottom: parent.bottom
        }

        Rectangle {
            id: canvas
            objectName: "canvas"

            width: 100

            color: "green"

            anchors.top: parent.top
            anchors.bottom: parent.bottom
        }
    }
}
