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
    room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
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
