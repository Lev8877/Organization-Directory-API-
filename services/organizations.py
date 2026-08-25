from models.activity import Activity

def get_activity_tree(activity: Activity) -> list[Activity]: 
    result = [activity]

    for child in activity.children:
        result.append(child)

        for grandchild in child.children:
            result.append(grandchild)

    return result 