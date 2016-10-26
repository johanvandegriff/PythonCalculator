#!/bin/bash

color() {
  color="$1"
  shift
  text="$@"
  case "$color" in
    # text attributes
#    end) num=0;;
    bold) num=1;;
    special) num=2;;
    italic) num=3;;
    underline|uline) num=4;;
    reverse|rev|reversed) num=7;;
    concealed) num=8;;
    strike|strikethrough) num=9;;

    # foreground colors
    black) num=30;;
    D_red) num=31;;
    D_green) num=32;;
    D_yellow) num=33;;
    D_blue) num=34;;
    D_magenta) num=35;;
    D_cyan) num=36;;
    gray) num=37;;

    D_gray) num=90;;
    red) num=91;;
    green) num=92;;
    yellow) num=93;;
    blue) num=94;;
    magenta) num=95;;
    cyan) num=96;;

    # background colors
    B_black) num=40;;
    BD_red) num=41;;
    BD_green) num=42;;
    BD_yellow) num=43;;
    BD_blue) num=44;;
    BD_magenta) num=45;;
    BD_cyan) num=46;;
    B_L_gray) num=47;;

    B_gray) num=100;;
    B_red) num=101;;
    B_green) num=102;;
    B_yellow) num=103;;
    B_blue) num=104;;
    B_magenta) num=105;;
    B_cyan) num=106;;
    B_white) num=107;;
    +([0-9])) num="$color";;
    *) echo "$text"
       return;;
  esac

  mycode='\033['"$num"'m'
  text=$(echo "$text" | sed -e 's,\[0m,\[0m\\033\['"$num"'m,g')
  echo -e "$mycode$text"'\033[0m'
}