from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalogitems.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create  user
User1 = User(name="latifa", email="latifa@udacity.com")
session.add(User1)
session.commit()

# Item for Action movies
category1 = Category(user_id=1, name="Action")

session.add(category1)
session.commit()

Item1 = Item(user_id=1, title="Mission Impossible Fallout",
            description="Ethan Hunt and his IMF team along with some familiar allies race against time after a mission gone wrong",  # noqa
            category=category1)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1, title="The Fate of the Furious",
            description="When a mysterious woman seduces Dom into the world of terrorism and a betrayal of those closest to him, the crew face trials that will test them as never before",  # noqa
            category=category1)

session.add(Item2)
session.commit()


# Item for Adventure movies
category2 = Category(user_id=1, name="Adventure")

session.add(category2)
session.commit()


Item2 = Item(user_id=1, title="Interstellar",
            description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival",  # noqa
            category=category2)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="Inception",
            description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO",  # noqa
            category=category2)

session.add(Item3)
session.commit()


# Item for Animation movies
category3 = Category(user_id=1, name="Animation")

session.add(category3)
session.commit()


Item2 = Item(user_id=1, title="Cars",
            description="A hot-shot race-car named Lightning McQueen gets waylaid in Radiator Springs, where he finds the true meaning of friendship and family",  # noqa
            category=category3)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="Monsters, Inc",
            description="In order to power the city, monsters have to scare children so that they scream. However, the children are toxic to the monsters, and after a child gets through, 2 monsters realize things may not be what they think",  # noqa
            category=category3)

session.add(Item3)
session.commit()


# Item for Crime movies
category4 = Category(user_id=1, name="Crime")

session.add(category4)
session.commit()


Item2 = Item(user_id=1, title="The Silence of the Lambs",
            description="A young FBI cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims",  # noqa
            category=category4)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="The Fugitive",
            description="MDr. Richard Kimble, unjustly accused of murdering his wife, must find the real killer while being the target of a nationwide manhunt lead by a seasoned US Marshall",  # noqa
            category=category4)

session.add(Item3)
session.commit()


# Item for Drama movies
category5 = Category(user_id=1, name="Drama")

session.add(category5)
session.commit()


Item1 = Item(user_id=1, title="The Green Mile",
            description="The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift",  # noqa
            category=category5)

session.add(Item1)
session.commit()


Item3 = Item(user_id=1, title="Black Swan",
            description="A committed dancer wins the lead role in a production of Tchaikovsky's Swan Lake only to find herself struggling to maintain her sanity",  # noqa
            category=category5)

session.add(Item3)
session.commit()


# Item for Fantasy movies
category6 = Category(user_id=1, name="Fantasy")

session.add(category6)
session.commit()


Item1 = Item(user_id=1, title="The Lord of the Rings",
            description="A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron",  # noqa
            category=category6)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title="The Curious Case of Benjamin Button",
            description="Tells the story of Benjamin Button, a man who starts aging backwards with bizarre consequences",  # noqa
            category=category6)

session.add(Item2)
session.commit()


# Item for War movies
category7 = Category(user_id=1, name="War")

session.add(category7)
session.commit()

Item1 = Item(user_id=1, title="Saving Private Ryan",
            description="Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action",  # noqa
            category=category7)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1, title="Hacksaw Ridge",
            description="World War American Army Medic Desmond Doss who served during the Battle of Okinawa refuses to kill people and becomes the first man in American history to receive the Medal of Honor without firing a shot",  # noqa
            category=category7)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="Fury",
            description="A grizzled tank commander makes tough decisions as he and his crew fight their way across Germany in April, 1945",  # noqa
            category=category7)

session.add(Item3)
session.commit()


# Item for Horror movies
category8 = Category(user_id=1, name="Horror")

session.add(category8)
session.commit()


Item2 = Item(user_id=1, title="The Exorcist",
            description="When a teenage girl is possessed by a mysterious entity, her mother seeks the help of two priests to save her daughter",  # noqa
            category=category8)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, title="The Ring",
            description="A journalist must investigate a mysterious videotape which seems to cause the death of anyone in a week of viewing it",  # noqa
            category=category8)

session.add(Item3)
session.commit()

# Item for Family movies
category9 = Category(user_id=1, name="Family")
session.add(category9)
session.commit()


Item2 = Item(user_id=1, title="The parent trap",
            description="Identical twins Annie and Hallie, separated at birth and each raised by one of their biological parents, later discover each other for the first time at summer camp and make a plan to bring their wayward parents back together",  # noqa
            category=category9)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1, title="Jumanji",
            description="When two kids find and play a magical board game, they release a man trapped for decades in it and a host of dangers that can only be stopped by finishing the game",  # noqa
            category=category9)

session.add(Item3)
session.commit()

# latest items
Item3 = Item(user_id=1, title="The Dark Knight",
            description="When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham. The Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice",  # noqa
            category=category1)

session.add(Item3)
session.commit()

Item1 = Item(user_id=1, title="Anni",
            description="A young orphan girl's adventures in finding a family that will take her",  # noqa
            category=category9)

session.add(Item1)
session.commit()

Item1 = Item(user_id=1, title="Saw",
            description="Two strangers, who awaken in a room with no recollection of how they got there, soon discover they're pawns in a deadly game perpetrated by a notorious serial killer",  # noqa
            category=category8)

session.add(Item1)
session.commit()

Item3 = Item(user_id=1, title="Avengers: Infinity War",
            description="The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe",  # noqa
            category=category6)

session.add(Item3)
session.commit()

Item2 = Item(user_id=1, title="The Shawshank Redemption",
            description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency",  # noqa
            category=category5)

session.add(Item2)
session.commit()

Item1 = Item(user_id=1, title="The Godfather",
            description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son",  # noqa
            category=category4)

session.add(Item1)
session.commit()

Item1 = Item(user_id=1, title="Despicable Me",
            description="When a criminal mastermind uses a trio of orphan girls as pawns for a grand scheme, he finds their love is profoundly changing him for the better",  # noqa
            category=category3)

session.add(Item1)
session.commit()

Item1 = Item(user_id=1, title="Cast Away",
            description="A FedEx executive must transform himself physically and emotionally to survive a crash landing on a deserted island",  # noqa
            category=category2)

session.add(Item1)
session.commit()
print "added category items!"
