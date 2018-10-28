from models import *

description = 'description test'
tip = 'tip testing'
stuff = {
    '白菜':'1个',
    '萝卜':'2个'
}
title = 'title testing'
steps = 'step1, test1, \n step2, test2 \n step3, test3'

data=Recipe(
    food=title,
    description=description,
    tip=tip,
    step=steps
)
session.add(data)
session.commit()

for k,v in list(stuff.items()):
    mat=Material(
        material=k,
        volume=v
    )
    mat.foods = [data]
    session.add(mat)

    session.commit()

