from signald import Signal

s = Signal("+32478055818")
s.send_group_message("Bm5PHf38NlOR8GYYJyUXYw==", "Jawadde!")

for m in s.receive_messages():
  print(m)
