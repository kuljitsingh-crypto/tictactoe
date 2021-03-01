from flask import Blueprint,render_template,request,current_app
from random import random,choice
from .geniusplayer import GeniusComputerPlayer
import json
game=Blueprint("game",__name__)

game_move_keeper={}

@game.route("/newgame",methods=['POST','GET'])
def newgame():
    verified=True if request.cookies.get("user",False) else False
    if request.method=="POST":
        mode=int(request.form.get("playmode"))
    return render_template("newgame.html" ,random=random(),mode=mode,verified=verified)

@game.route("/newgame/hardmode",methods=["POST","GET"])
def hardMode():
    if request.method=="POST":
        if(request.is_json):
            user_req=request.get_json()
            user_id=str(user_req["user_id"])
            if(user_req.get("delete_obj",False)):
                try:
                    del(game_move_keeper[user_id])
                    return current_app.response_class(status=200) 
                except KeyError:pass
            else:
                if not(game_move_keeper.get(user_id,False)):
                    game_obj=GeniusComputerPlayer(user_req["letter"],user_req["board"],user_req["available_pos"],user_req["game_tie"])
                    game_move_keeper[user_id]={"game_obj":game_obj}
                    pos={"pos":game_obj.make_move()}

                else:
                    game_obj=game_move_keeper[user_id]["game_obj"]
                    game_obj.board=user_req["board"]
                    game_obj.available_pos=user_req["available_pos"]
                    game_obj.game_tie=user_req["game_tie"]
                    pos={"pos":game_obj.make_move()}

        res=current_app.response_class(response=json.dumps(pos),status=200,mimetype="application/json")
        return res
    
    return current_app.response_class(status=500)       

