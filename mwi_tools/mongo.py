from mwi_tools.coordinates import calculate as mwicc

def set_heading_and_speed_positions(races, race_name, id) : 
    a = races.aggregate([
        { "$match": {"name" : race_name} },
        { "$unwind": "$boats" },
        { "$match": { "boats.id": id } },
        { "$project": { "_id": 0, "boats.positions": 1 } },
    ]);
    positions = list(a)[0]['boats']['positions']
    positions.sort(key=lambda x : x['timestamp'])
    if len(positions)>0 : 
        positions[0]['heading'] = 0
        positions[0]['speed'] = 0
    for i in range(1,len(positions)) : 
        pos = positions[i]
        t_end = pos['timestamp']
        lat_end = pos['lat']
        lon_end = pos['lon']
        pos2 = positions[i-1]
        t_start = pos2['timestamp']
        lat_start = pos2['lat']
        lon_start = pos2['lon']

        if (t_end-t_start == 0) : 
            speed = 0
        else : 
            speed = mwicc.get_speed([lat_start,lon_start], [lat_end,lon_end], t_end-t_start)
        heading = mwicc.get_heading([lat_start,lon_start], [lat_end,lon_end])
        if (heading == None) and ('heading' in pos2): 
            pos['heading'] = pos2['heading']
        elif (heading == None) : 
            pos['heading'] = 0
        else : 
            pos['heading'] = heading

        pos['speed'] = speed
        positions[i] = pos
    
    races.update_one({"name" : race_name},{"$set":{"boats.$[elem].positions":positions}}, array_filters= [{ "elem.id": int(id)}])
    if len(positions)>0 : 
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].last_timestamp":positions[-1]['timestamp']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].rank":positions[-1]['rank']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].heading":positions[-1]['heading']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].speed":positions[-1]['speed']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].distToGoal":positions[-1]['distToGoal']}}, array_filters= [{ "elem.id": int(id)}])


def set_heading_and_speed_journal(races, race_name, id) : 
    a = races.aggregate([
        { "$match": {"name" : race_name} },
        { "$unwind": "$boats" },
        { "$match": { "boats.id": id } },
        { "$project": { "_id": 0, "boats.positions_journal": 1 } },
    ]);
    positions = list(a)[0]['boats']['positions_journal']
    positions.sort(key=lambda x : x['timestamp'])
    if len(positions)>0 : 
        positions[0]['heading'] = 0
        positions[0]['speed'] = 0
    for i in range(1,len(positions)) : 
        pos = positions[i]
        t_end = pos['timestamp']
        lat_end = pos['lat']
        lon_end = pos['lon']
        pos2 = positions[i-1]
        t_start = pos2['timestamp']
        lat_start = pos2['lat']
        lon_start = pos2['lon']

        speed = mwicc.get_speed([lat_start,lon_start], [lat_end,lon_end], t_end-t_start)
        heading = mwicc.get_heading([lat_start,lon_start], [lat_end,lon_end])
        if (heading == None) and ('heading' in pos2): 
            pos['heading'] = pos2['heading']
        elif (heading == None) : 
            pos['heading'] = 0
        else : 
            pos['heading'] = heading

        pos['speed'] = speed
        positions[i] = pos
    
    races.update_one({"name" : race_name},{"$set":{"boats.$[elem].positions_journal":positions}}, array_filters= [{ "elem.id": int(id)}])
    if len(positions)>0 : 
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].last_timestamp_journal":positions[-1]['timestamp']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].heading_journal":positions[-1]['heading']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].speed_journal":positions[-1]['speed']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].boat_speed_journal":positions[-1]['boat_speed']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].COG_journal":positions[-1]['COG']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].SOG_journal":positions[-1]['SOG']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].wind_speed_journal":positions[-1]['wind_speed']}}, array_filters= [{ "elem.id": int(id)}])
        races.update_one({"name" : race_name},{"$set":{"boats.$[elem].wind_dir_journal":positions[-1]['wind_dir']}}, array_filters= [{ "elem.id": int(id)}])

