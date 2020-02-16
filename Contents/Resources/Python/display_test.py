# -*- coding: utf-8 -*-
import kjams


def main():
    # test Message dialog
    if False:
        kjams.dialog_message("This is the message")

    # test OK_Cancel dialog
    if False:
        if kjams.dialog_ok_cancel("Press a button!"):
            kjams.dialog_message("You pressed OK!")
        else:
            kjams.dialog_message("You pressed Cancel!")

    # test full power of the 3 button dialog
    if True:
        buttonType = kjams.enum_button_type()
        test = kjams.get_volume()
        print test

        resultArray = kjams.dialog_three_button(
            "Awesome Dialog",
            str(test),
            "Ridiculous!", buttonType.kButtonType_CANCEL,
            "Very well", 0,
            "Superb!", buttonType.kButtonType_DEFAULT,
            "Check me if you wish", False)

        buttonNumber = resultArray[0]  # 1, 2, or 3
        checkB = resultArray[1]  # True or False
        buttonName = resultArray[2]  # name of button that was pressed

        resultStr = "You pressed the “" + buttonName + "” button, and the check box was "
        if checkB:
            resultStr += "CHECKED!"
        else:
            resultStr += "NOT checked!"

        kjams.dialog_message(resultStr)

    # test input dialog
    if True:
        resultArray = kjams.dialog_input("A Question for you!", "What is your favorite colour?", "Blue", False)
        okayB = resultArray[0]  # True or False
        outputStr = resultArray[1]  # what the user typed

        resultStr = "You pressed "
        if okayB:
            resultStr += "OK, and you typed “" + outputStr + "”."
        else:
            resultStr += "Cancel"

        kjams.dialog_message(resultStr)


# -----------------------------------------------------
if __name__ == "__main__":
    main()
