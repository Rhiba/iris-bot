import ..utils.randomperks

def randomperks(db_sesson, message, *args):
    try:
        if not args:
             raise Exception("Use !randomperks killer or !randomperks survivor")
        else:
            return utils.randomperks.get_perks(args[0])
    except Exception as e:
        print("exception")
        return [str(e)]
