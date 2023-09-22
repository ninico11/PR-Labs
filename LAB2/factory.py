from player import Player
import dicttoxml
import player_pb2
import xml.etree.ElementTree as ET


class PlayerFactory:
    def to_json(self, players):
        player_list = []
        for player in players:
            key_list = {"nickname": None, "email": None, "date_of_birth": None, "xp": None, "class": None}
            key_list["nickname"] = player.nickname
            key_list["email"] = player.email
            key_list["date_of_birth"] = player.date_of_birth.strftime("%Y-%m-%d")
            key_list["xp"] = player.xp
            key_list["class"] = player.cls
            player_list.append(key_list)
        return player_list

    def from_json(self, list_of_dict):
        player_list = []
        for i in list_of_dict:
            player = Player(i["nickname"], i["email"], i["date_of_birth"], i["xp"], i["class"])
            player_list.append(player)
        return player_list

    def from_xml(self, xml_string):
        root = ET.fromstring(xml_string)
        players_dict = []
        for player in root:
            for attribute in player:
                if attribute.tag == "nickname":
                    name = attribute.text
                if attribute.tag == "email":
                    email = attribute.text
                if attribute.tag == "date_of_birth":
                    dob = attribute.text
                if attribute.tag == "xp":
                    xp = attribute.text
                if attribute.tag == "class":
                    cls = attribute.text
            newobj = Player(name, email, dob, int(xp), cls)
            players_dict.append(newobj)
        return players_dict

    def to_xml(self, list_of_players):

        players_dicts = []

        for player in list_of_players:
            player.date_of_birth = player.date_of_birth.strftime('%Y-%m-%d')
            player_atrr = vars(player)
            player_atrr['class'] = player_atrr['cls']
            del player_atrr['cls']
            players_dicts.append(player_atrr)

        xml = dicttoxml.dicttoxml(players_dicts, attr_type=False, custom_root='data', item_func=lambda x: 'player')

        return xml

    def from_protobuf(self, binary):
        players_list = player_pb2.PlayersList()
        players_list.ParseFromString(binary)

        list_of_players = []

        for item in players_list.player:
            list_of_players.append(Player(
                item.nickname,
                item.email,
                item.date_of_birth,
                item.xp,
                player_pb2.Class.Name(item.cls)
            ))

        return list_of_players

    def to_protobuf(self, list_of_players):
        players_list = player_pb2.PlayersList()

        for player in list_of_players:
            proto_player = players_list.player.add()

            setattr(proto_player, 'nickname', player.nickname)
            setattr(proto_player, 'email', player.email)
            setattr(proto_player, 'date_of_birth', player.date_of_birth.strftime("%Y-%m-%d"))
            setattr(proto_player, 'xp', player.xp)
            setattr(proto_player, 'cls', getattr(player_pb2.Class, player.cls))

        return players_list.SerializeToString()
