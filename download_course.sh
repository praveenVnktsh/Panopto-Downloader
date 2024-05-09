COURSEID="PGM"
BASEURL="https://scs.hosted.panopto.com"
TABLEURL="https://scs.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx#view=0&folderID=%22fc22c4da-73d0-4c60-b221-b0f900f9ac93%22&page=0&maxResults=150"

python3 download.py --baseurl $BASEURL --courseid $COURSEID --tableurl $TABLEURL
