from django.contrib.auth.models import User
from adventure.models import Player, Room

Room.objects.all().delete()

size_y = 8
size_x = 13
num_rooms = 100

grid = [None] * size_y
width = size_x
height = size_y
for i in range(len(grid)):
    grid[i] = [None] * size_x

x = -1  # (this will become 0 on the first step)
y = 0
room_count = 0

# Start generating rooms to the east
direction = 1  # 1: east, -1: west

# While there are rooms to be created...
previous_room = None
while room_count < num_rooms:

    # Calculate the direction of the room to be created
    if direction > 0 and x < size_x - 1:
        room_direction = "e"
        reverse_direction = "w"
        x += 1
    elif direction < 0 and x > 0:
        room_direction = "w"
        reverse_direction = "e"
        x -= 1
    else:
        # If we hit a wall, turn north and reverse direction
        room_direction = "n"
        reverse_direction = "s"
        y += 1
        direction *= -1
    # Create a room in the given direction
    travel = ""
    if x > 0 and x < size_x - 1:
        travel = "east and west."
    if x == size_x - 1 and direction > 0:
        travel = "north and west."
    if x == size_x - 1 and direction < 0:
        travel = "south and west."
    if x == 0 and direction < 0:
        travel = "north and east."
    if x == 0 and direction > 0:
        travel = "south and east."
    if room_count == 0:
        travel = "east"
    if room_count == num_rooms-1:
        if direction < 0:
            travel = "east"
        if direction > 0:
            travel = "west"
    room = Room(room_count+1, f"Room #{room_count+1}",
                f"This is room #{room_count+1}. From here you can travel {travel}", x, y)
    # Note that in Django, you'll need to save the room after you create it
    # Save the room in the World grid
    grid[y][x] = room
    # Connect the new room to the previous room
    room.save()
    if previous_room is not None:
        previous_room.connectRooms(room, room_direction)
        room.connectRooms(previous_room, reverse_direction)
    # Update iteration variables
    previous_room = room
    room_count += 1
