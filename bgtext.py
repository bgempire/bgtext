""" BGText - A Dynamic Text Utility for Blender Game Engine

Author: Joel Gomes da Silva
BA Profile: https://blenderartists.org/u/joelgomes1994/ """

import bge
import os
from textwrap import wrap
from pprint import pprint, pformat
from bge.logic import globalDict, LibNew
from mathutils import Matrix
from ast import literal_eval
from time import time

bge.logic.aboutBGText = "BGText: A BGE Dynamic Text Utility"

### Constants ###
DBG = 0
CHARS_X = 16
CHARS_Y = 8
CHARS_TABLE = {
    '!' : (0,0), '"' : (1,0), '#' : (2,0), '$' : (3,0), '%' : (4,0), '&' : (5,0), "'" : (6,0), '(' : (7,0), ')' : (8,0), '*' : (9,0), '+' : (10,0), ',' : (11,0), '-' : (12,0), '.' : (13,0), '/' : (14,0), '0' : (15,0), 
    '1' : (0,1), '2' : (1,1), '3' : (2,1), '4' : (3,1), '5' : (4,1), '6' : (5,1), '7' : (6,1), '8' : (7,1), '9' : (8,1), ':' : (9,1), ';' : (10,1), '<' : (11,1), '=' : (12,1), '>' : (13,1), '?' : (14,1), '@' : (15,1), 
    'A' : (0,2), 'B' : (1,2), 'C' : (2,2), 'D' : (3,2), 'E' : (4,2), 'F' : (5,2), 'G' : (6,2), 'H' : (7,2), 'I' : (8,2), 'J' : (9,2), 'K' : (10,2), 'L' : (11,2), 'M' : (12,2), 'N' : (13,2), 'O' : (14,2), 'P' : (15,2), 
    'Q' : (0,3), 'R' : (1,3), 'S' : (2,3), 'T' : (3,3), 'U' : (4,3), 'V' : (5,3), 'W' : (6,3), 'X' : (7,3), 'Y' : (8,3), 'Z' : (9,3), '[' : (10,3), '\\': (11,3), ']' : (12,3), '^' : (13,3), '_' : (14,3), '`' : (15,3), 
    'a' : (0,4), 'b' : (1,4), 'c' : (2,4), 'd' : (3,4), 'e' : (4,4), 'f' : (5,4), 'g' : (6,4), 'h' : (7,4), 'i' : (8,4), 'j' : (9,4), 'k' : (10,4), 'l' : (11,4), 'm' : (12,4), 'n' : (13,4), 'o' : (14,4), 'p' : (15,4), 
    'q' : (0,5), 'r' : (1,5), 's' : (2,5), 't' : (3,5), 'u' : (4,5), 'v' : (5,5), 'w' : (6,5), 'x' : (7,5), 'y' : (8,5), 'z' : (9,5), '{' : (10,5), '|' : (11,5), '}' : (12,5), '~' : (13,5), '¡' : (14,5), '¢' : (15,5), 
    '£' : (0,6), '¥' : (1,6), '©' : (2,6), '®' : (3,6), 'À' : (4,6), 'Á' : (5,6), 'Â' : (6,6), 'Ã' : (7,6), 'Ç' : (8,6), 'É' : (9,6), 'Ê' : (10,6), 'Í' : (11,6), 'Ñ' : (12,6), 'Ó' : (13,6), 'Ô' : (14,6), 'Õ' : (15,6), 
    'Ú' : (0,7), 'Ü' : (1,7), 'à' : (2,7), 'á' : (3,7), 'â' : (4,7), 'ã' : (5,7), 'ç' : (6,7), 'é' : (7,7), 'ê' : (8,7), 'í' : (9,7), 'ñ' : (10,7), 'ó' : (11,7), 'ô' : (12,7), 'õ' : (13,7), 'ú' : (14,7), 'ü' : (15,7)
}
COLORS = {
    "WHITE" : (1, 1, 1, 1),
    "RED" : (1, 0, 0, 1),
    "GREEN" : (0, 1, 0, 1),
    "BLUE" : (0, 0, 1, 1),
    "YELLOW" : (1, 1, 0, 1),
    "PURPLE" : (1, 0, 1, 1),
    "CYAN" : (0, 1, 1, 1),
    "BLACK" : (0, 0, 0, 1)
}

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def createCharLib(cont, char, mesh, style):
    own = cont.owner
    
    # Create a new mesh lib for current character
    libName = str(style) + "-" + str(ord(char))
    mesh = LibNew(libName, "Mesh", [mesh.name])[0]
    
    ### Transform UV of created mesh to fit corresponding char ###
    # Scale UV to single character size (horizontally)
    transformMatrix = Matrix.Scale(1/CHARS_X, 4, (1, 0, 0))
    mesh.transformUV(-1, transformMatrix)
    
    # Scale UV to single character size (vertically)
    transformMatrix = Matrix.Scale(1/CHARS_Y, 4, (0, 1, 0))
    mesh.transformUV(-1, transformMatrix)
    
    # Move UV to the top left of texture (first character)
    transformMatrix = Matrix.Translation((0, CHARS_Y-(1/CHARS_Y), 0))
    mesh.transformUV(-1, transformMatrix)
    
    # Translate UV to the respective position of char in chars table
    x, y = CHARS_TABLE[char][0], CHARS_TABLE[char][1]
    transformMatrix = Matrix.Translation((x/CHARS_X, CHARS_Y-(y/CHARS_Y), 0))
    mesh.transformUV(-1, transformMatrix)
    
    ### Store created mesh reference in scene for current style ###
    if not style in own.scene["CharLib"].keys():
        own.scene["CharLib"][style] = {}
        
    own.scene["CharLib"][style][ord(char)] = mesh
    
def createCharLibInScene(cont):
    own = cont.owner
    
    for i in range(1, 6):
        
        # The temp char object will provide the base mesh for the libs creation
        tempChar = own.scene.addObject("_TxtChar" + str(i))
        mesh = tempChar.meshes[0]
        
        # Create a mesh lib for each char in chars table
        for char in CHARS_TABLE.keys():
            
            try:
                createCharLib(cont, char, mesh, i)
                
            except:
                if DBG: print("x Error in char", char, ", style", i)
                return
                
        # End the temp char previously added
        tempChar.endObject()
        
        if DBG: print("  > Created lib for style", i, "on scene", own.scene.name)
        
def evalColor(txtColor):
    try:
        # Try to get a literal color if string starts with [ or (
        if txtColor.startswith('[') or txtColor.startswith('('):
            
            # Tries to eval given literal RGBA
                txtColor = literal_eval(txtColor)
                
                # Ensures valid RGBA after eval
                if len(txtColor) != 4:
                    raise Exception
                
        # Get color from colors table if exists
        elif txtColor.upper() in COLORS.keys():
            txtColor = COLORS[txtColor.upper()]
            
        # Defaults to white otherwise
        else:
            raise Exception
            
    # Defaults to white if could not eval color
    except:
        txtColor = COLORS["WHITE"]
        
    return txtColor

def getPropsFromGroup(cont):
    own = cont.owner
    always = cont.sensors["Always"]
    
    ### Get and set simple properties from group ###
    own["Size"] = own.groupObject["Size"] if "Size" in own.groupObject else own["Size"]
    own["Offset"] = own.groupObject["Offset"] if "Offset" in own.groupObject else own["Offset"]
    own["OffsetH"] = own.groupObject["OffsetH"] if "OffsetH" in own.groupObject else own["Offset"]
    own["OffsetV"] = own.groupObject["OffsetV"] if "OffsetV" in own.groupObject else own["Offset"]
    own["Wrap"] = own.groupObject["Wrap"] if "Wrap" in own.groupObject else own["Wrap"]
    own["Justify"] = own.groupObject["Justify"] if "Justify" in own.groupObject else own["Justify"]
    own["Style"] = clamp(own.groupObject["Style"], 1, 5) if "Style" in own.groupObject else own["Style"]
    
    if "Id" in own.groupObject:
        own["Id"] = own.groupObject["Id"]
        
    # Get the Update property and set it to the always sensor
    if "Update" in own.groupObject:
        own["Update"] = own.groupObject["Update"] if type(own.groupObject["Update"]) == int else -1
        
        # Enable pulse mode on always sensor and set update interval to it
        if own["Update"] >= 0 and not always.usePosPulseMode:
            always.usePosPulseMode = True
            always.skippedTicks = own["Update"]
            
        # Disable pulse mode on always sensor and set update interval to zero
        elif own["Update"] < 0 and always.usePosPulseMode:
            always.usePosPulseMode = False
            always.skippedTicks = 0
        
    if not "LastColor" in own:
        own["LastColor"] = "WHITE"
        own["ColorEval"] = (1, 1, 1, 1)
            
    ### Get and process the Color property from group ###
    if "Color" in own.groupObject:
        if own.groupObject["Color"] != own["LastColor"]:
            own["ColorEval"] = evalColor(own.groupObject["Color"])
            own["LastColor"] = own.groupObject["Color"]
            
    elif not "Color" in own.groupObject:
        if own["Color"] != own["LastColor"]:
            own["LastColor"] = own["Color"]
            own["ColorEval"] = evalColor(own["Color"])
    
    ### Get Text from group ###
    if "Text" in own.groupObject:
        targetText = str(own.groupObject["Text"])
        
        # Tries to get a text reference if starts with eval char
        if targetText.startswith('>'):
            
            # Tries to eval reference from string
            try:
                own["Text"] = str(eval(targetText.strip('>')))
                
            # Set Text to literal if cannot eval string
            except:
                own["Text"] = targetText
                
        # Set Text to literal value if not starts with eval char
        else:
            own["Text"] = targetText
        
def getTextJustified(cont, asString=False):
    own = cont.owner
    finalText = wrap(own["Text"], own["Wrap"])
    linesJust = []
    
    # Iterates over lines indexes
    for _line in finalText:
        
        # Center justify
        if own["Justify"].lower() == 'center':
            _line = _line.center(own["Wrap"])
        
        # Right justify
        elif own["Justify"].lower() == 'right':
            _line = _line.rjust(own["Wrap"])
        
        linesJust.append(_line)
            
    return linesJust if not asString else "\n".join(linesJust)
        
def addChar(cont):
    obj = cont.owner.scene.addObject("_TxtCharBlank", cont.owner)
    obj.setParent(cont.owner)
    return obj

def updateChar(cont, obj, char, x, y):
    own = cont.owner
    
    if obj["Char"] != ord(char) or own["LastStyle"] != own["Style"]:
        obj["Char"] = ord(char)
        
        if obj["Char"] in own.scene["CharLib"][own["Style"]].keys():
            charMesh = own.scene["CharLib"][own["Style"]][obj["Char"]]
            obj.replaceMesh(charMesh)
        
    obj.color = own["ColorEval"]
    obj.visible = not char in (" ", "\t", "\n")
    obj.localPosition.x = x * own["OffsetH"]
    obj.localPosition.y = y * own["OffsetV"]
    obj.localScale = (own["Size"], own["Size"], 1.0)

def equalizeLines(cont, textLines):
    own = cont.owner
    
    # Remove exceeding chars if more than target text chars
    if len(own["Chars"]) > len(textLines):
        if DBG: print("  > Number of lines is > than new text on:", own.groupObject)
        for charObj in own["Chars"][len(textLines):]:
            charObj.endObject()
        own["Chars"] = own["Chars"][0:len(textLines)]
        
    # Add missing chars if less than target text chars
    elif len(own["Chars"]) < len(textLines):
        if DBG: print("  > Number of lines is < than new text on:", own.groupObject)
        for i in range(len(own["Chars"]), len(textLines)):
            own["Chars"].append(addChar(cont))
    
def updateText(cont):
    own = cont.owner
    
    # Wrap and justify final text in different lines
    textLines = getTextJustified(cont, asString=True)
    
    # Fit the number of lines and char objs to text lines
    equalizeLines(cont, textLines)
    
    x, y = 0, 0
    
    for i in range(len(textLines)):
        
        updateChar(cont, own["Chars"][i], textLines[i], x, y)
        x += 1
            
        if textLines[i] == "\n":
            x = 0
            y -= 1
            
    own["LastStyle"] = own["Style"]
        
    if DBG: print("  > Text updated:", own.groupObject)
        
### Main Functions ###
def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
    always = cont.sensors["Always"]
    message = cont.sensors["Message"]
    
    startTime = time()
    
    # End object if not a group instance
    if own.groupObject is None:
        own.endObject()
        return
        
    if always.positive and always.status == 1 or message.positive or own["Update"] >= 0:
        
        if "Disabled" in own.groupObject:
            if own.groupObject["Disabled"]:
                return
        
        if DBG: print("> Running text object", own.groupObject)
        
        if not "Chars" in own:
            own["Chars"] = []
        
        # Parent manager to group instance if not already
        if own.parent != own.groupObject:
            own.setParent(own.groupObject)
            
        # Get and set properties from group to owner
        getPropsFromGroup(cont)
            
        # Creates the mesh library for all characters of current style
        # Create char lib dict in scene to store char meshes
        if not "CharLib" in own.scene:
            own.scene["CharLib"] = {}
            createCharLibInScene(cont)
            
        # Exit function if not all chars from table were created as libs
        if len(own.scene["CharLib"][own["Style"]].keys()) != len(CHARS_TABLE.keys()):
            return
            
        if message.positive:
            bodies = [b for b in message.bodies]
            
            if own["Id"] in bodies or "All" in bodies:
                updateText(cont)
                own["LastText"] = own["Text"]
        
        else:
            if own["Update"] >= 0:
                updateText(cont)
                own["LastText"] = own["Text"]
            
            elif len(own["Text"]) > 0 and own["Text"] != own["LastText"]:
                updateText(cont)
                own["LastText"] = own["Text"]
            
        if DBG:
            print("  > Ran", own.groupObject, ", time taken:", round(time() - startTime, 4), "seconds")
  
# Uncomment below when running on controller in Script mode
# or call the main function on the controller if running Module mode
main()