# AmberHan
# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2021/4/26 10:57
# !@File   : zqDecisionTree.py
#决策树

# mylistVehicle = [0.0, 0.0, 0.0]
# mylistFacial = [0.0, 0.0, 0.0]
# mylistVocal = [0.0]

def riskMode(mylistVehicle,mylistFacial,mylistVocal):

    # 驾驶数据
    levelVehicle = "G"
    if (mylistVehicle[0] > 0.9
            or mylistVehicle[1] > 0.9
            or mylistVehicle[2] > 0.9):
        levelVehicle = "RR"
        return "RR"
    else:
        iNum = 0
        iNum += (1 if mylistVehicle[0] > 0.7 else 0)
        iNum += (1 if mylistVehicle[1] > 0.7 else 0)
        iNum += (1 if mylistVehicle[2] > 0.7 else 0)
        if iNum >= 2:
            levelVehicle = "RR"
            return "RR"
        elif iNum == 1:
            levelVehicle = "R"
        else:
            iNum = 0
            iNum += (1 if mylistVehicle[0] > 0.5 else 0)
            iNum += (1 if mylistVehicle[1] > 0.5 else 0)
            iNum += (1 if mylistVehicle[2] > 0.5 else 0)
            if iNum >= 2:
                levelVehicle = "R"
            elif iNum == 1:
                levelVehicle = "Y"

    # 面部表情+语音
    levelFacialVocal = "G"
    if (mylistFacial[0] > 0.91
            or mylistFacial[1] > 0.91
            or mylistFacial[2] > 0.91
            or mylistVocal[0] > 0.91
    ):
        levelFacialVocal = "RR"
        return "RR"
    else:
        iNum = 0;
        iNum += (1 if mylistFacial[0] > 0.8 else 0)
        iNum += (1 if mylistFacial[1] > 0.8 else 0)
        iNum += (1 if mylistFacial[2] > 0.8 else 0)
        iNum += (1 if mylistVocal[0] > 0.8 else 0)
        if iNum >= 2:
            levelFacialVocal = "RR"
            return "RR"
        elif iNum == 1:
            levelFacialVocal = "R"
        else:
            iNum = 0;
            iNum += (1 if mylistFacial[0] > 0.6 else 0)
            iNum += (1 if mylistFacial[1] > 0.6 else 0)
            iNum += (1 if mylistFacial[2] > 0.6 else 0)
            iNum += (1 if mylistVocal[0] > 0.6 else 0)
            if iNum >= 2:
                levelFacialVocal = "R"
            elif iNum == 1:
                levelFacialVocal = "Y"

    iNum = 0;
    iNum += (1 if levelVehicle == "R" else 0)
    iNum += (1 if levelFacialVocal == "R" else 0)
    if iNum == 2:
        return "RR"
    elif iNum == 1:
        return "R"
    else:
        iNum = 0
        iNum += (1 if levelVehicle == "Y" else 0)
        iNum += (1 if levelFacialVocal == "Y" else 0)
        if iNum == 2:
            return "R"
        elif iNum == 1:
            return "Y"
    return "G"


if __name__ == '__main__':
    mylistVehicle = [0.9, 0.8, 0.0]
    mylistFacial = [0.1, 0.0, 0.0]
    mylistVocal = [0.8]

    ret= riskMode(mylistVehicle, mylistFacial, mylistVocal)
    print(ret)