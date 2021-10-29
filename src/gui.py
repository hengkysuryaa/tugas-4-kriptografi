import PySimpleGUI as sg
import rsa, paillier, elgamal, ecc

def saveFile(path, content):
    with open("../keys/"+path, 'w') as file:
        file.write(content)

sg.theme("Reddit")
layout = [
    [sg.T("Tucil 4 Kriptografi Modern", font="Any 20")],
    [sg.TabGroup([[
        sg.Tab("RSA", [
            [sg.Text("Generate Keys", font="Any 10")],
            [sg.T("P (prime)", size=(8, 1)), sg.In(key="p_val_rsa", size=(60, 1))],
            [sg.T("Q (prime)", size=(8, 1)), sg.In(key="q_val_rsa", size=(60, 1))],
            [sg.Text("Output Keys", font="Any 10")],
            [sg.T("Public", size=(8, 1)), sg.In(key="public_out_rsa", size=(60, 1))],
            [sg.T("Private", size=(8, 1)), sg.In(key="private_out_rsa", size=(60, 1))],
        ], key="RSA"),
        sg.Tab("Elgamal", [
            [sg.Text("Generate Keys", font="Any 10")],
            [sg.T("P (prime)", size=(8, 1)), sg.In(key="p_val_elgamal", size=(60, 1))],
            [sg.Text("Output Keys", font="Any 10")],
            [sg.T("Public", size=(8, 1)), sg.In(key="public_out_elgamal", size=(60, 1))],
            [sg.T("Private", size=(8, 1)), sg.In(key="private_out_elgamal", size=(60, 1))],
        ], key="Elgamal"),
        sg.Tab("Paillier", [
            [sg.Text("Generate Keys", font="Any 10")],
            [sg.T("P (prime)", size=(8, 1)), sg.In(key="p_val_paillier", size=(60, 1))],
            [sg.T("Q (prime)", size=(8, 1)), sg.In(key="q_val_paillier", size=(60, 1))],
            [sg.Text("Output Keys", font="Any 10")],
            [sg.T("Public", size=(8, 1)), sg.In(key="public_out_paillier", size=(60, 1))],
            [sg.T("Private", size=(8, 1)), sg.In(key="private_out_paillier", size=(60, 1))],
        ], key="Paillier"),
        sg.Tab("ECEG", [
            [sg.Text("Generate Keys | Equation y^2 = x^3 + ax + b mod p", font="Any 10")],
            [   sg.T("a", size=(2, 1)), sg.In(key="a_val_eceg", size=(5, 1)),
                sg.T("b", size=(2, 1)), sg.In(key="b_val_eceg", size=(5, 1)),
                sg.T("p", size=(2, 1)), sg.In(key="p_val_eceg", size=(5, 1)),
                sg.Button("GenerateElipticGroup", pad=(5, 10)),
                sg.Text("Eliptic Group List", font="Any 10"), sg.Multiline(key="eliptic_group_list", size=(30, 3)),
            ],
            [sg.T("Chosen BasePoint", size=(15, 1)), sg.In(key="base_point_eceg", size=(15, 1))],
            [sg.Text("Output Keys", font="Any 10")],
            [sg.T("Public", size=(8, 1)), sg.In(key="public_out_eceg", size=(60, 1))],
            [sg.T("Private", size=(8, 1)), sg.In(key="private_out_eceg", size=(60, 1))],
        ], key="ECEG"),
    ]], key="current_action")],
    [
        sg.Button("GenerateKey", pad=(5, 10)),
        sg.T("Filename", size=(8, 1)),
        sg.In(key="filename", size=(25, 1)),
        sg.Button("SavePublicKey", pad=(5, 10)),
        sg.Button("SavePrivateKey", pad=(5, 10))
    ],
    [sg.Text("", key="Info")],
    [sg.T("Input", size=(5, 1)), sg.Multiline(key="input_text", size=(35, 7)), sg.T("Output", size=(5, 1)), sg.Multiline(key="output_text", size=(35, 7))],
    [sg.T("Key", size=(5, 1)), sg.In(key="key", size=(60, 1)), sg.Button("BrowseKey", pad=(5, 10))],
    [sg.Button("Encrypt", pad=(5, 10)), sg.Button("Decrypt", pad=(5, 10))],
]

window = sg.Window("Tucil 4", layout)
# event, values = window.read()
while True:
    event, values = window.read(timeout = 10)
    event = event.lower()
    window["Info"].update("Encrypt/Decrypt using: " + str(values["current_action"]))
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    if event == "generatekey":
        #print(event)
        #print("Action:", values["current_action"])
        #window["Info"].update("do key"+str(values["current_action"]))
        current_mode = values["current_action"]
        if current_mode == "RSA":
            keys = rsa.generateKey(int(values["p_val_rsa"]), int(values["q_val_rsa"]))
            if keys == None:
                window["public_out_rsa"].update("p,q tidak prima")
                window["private_out_rsa"].update("p,q tidak prima")
            else:
                window["public_out_rsa"].update(keys["public"])
                window["private_out_rsa"].update(keys["private"])
        if current_mode == "Elgamal":
            keys = elgamal.generateKey(int(values["p_val_elgamal"]))
            if keys == None:
                window["public_out_elgamal"].update("p tidak prima")
                window["private_out_elgamal"].update("p tidak prima")
            else:
                window["public_out_elgamal"].update(keys["public"])
                window["private_out_elgamal"].update(keys["private"])
        if current_mode == "Paillier":
            keys = paillier.generateKey(int(values["p_val_paillier"]), int(values["q_val_paillier"]))
            if keys == None:
                window["public_out_paillier"].update("p, q tidak memenuhi syarat")
                window["private_out_paillier"].update("p, q tidak memenuhi syarat")
            else:
                window["public_out_paillier"].update(keys["public"])
                window["private_out_paillier"].update(keys["private"])
        if current_mode == "ECEG":
            basePoint = values["base_point_eceg"].replace('(','').replace(')','').split(",")
            keys = ecc.generateKey(int(values["a_val_eceg"]), int(values["b_val_eceg"]), int(values["p_val_eceg"]), int(basePoint[0]), int(basePoint[1]))
            if keys == None:
                window["public_out_eceg"].update("base point tidak memenuhi syarat")
                window["private_out_eceg"].update("base point tidak memenuhi syarat")
            else:
                window["public_out_eceg"].update(keys["public"])
                window["private_out_eceg"].update(keys["private"])
        
    if event == "generateelipticgroup":
        eg = ecc.generateElipticGroup(int(values["a_val_eceg"]), int(values["b_val_eceg"]), int(values["p_val_eceg"]))
        window["eliptic_group_list"].update(eg)
        #print(eg)
        #keys = ecc.generateKey(int(values["p_val_paillier"]), int(values["q_val_paillier"]))
    if event == "savepublickey":
        if values["filename"] == "":
            window["filename"].update("filename kosong")
        else:
            contentLoc = "public_out_" + current_mode.lower()
            saveFile(values["filename"], values[contentLoc])
            window["filename"].update("tersimpan di folder keys")

    if event == "saveprivatekey":
        if values["filename"] == "":
            window["filename"].update("filename kosong")
        else:
            contentLoc = "private_out_" + current_mode.lower()
            saveFile(values["filename"], values[contentLoc])
            window["filename"].update("tersimpan di folder keys")

    if event == "encrypt":
        # IF per action
        window["Info"].update("do enc "+str(values["current_action"]))
    if event == "decrypt":
        window["Info"].update("do dec "+str(values["current_action"]))