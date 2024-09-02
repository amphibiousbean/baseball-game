class Batter:
    #name : their name
    #pow : ability to hit for power
    #con : ability to make solid contact
    #vis : ability to foul off pitches and avoid swinging and missing
    #disc : ability to take balls and not swing at bad pitches
    def __init__(self, name, pow, con, vis, disc):
        self.type = "Batter"
        self.name = name
        self.pow = pow
        self.con = con
        self.vis = vis
        self.disc = disc

    def print(self):
        r = str(self.name) +  "\nPower :  " + str(self.pow) + "\nContact : " + str(self.con) + "\nVision : " + str(self.vis) + "\nDiscipline : " + str(self.disc)
        print(r)

    def toString(self):
        r = str(self.name) +  "\nPower :  " + str(self.pow) + "\nContact : " + str(self.con) + "\nVision : " + str(self.vis) + "\nDiscipline : " + str(self.disc)
        return r