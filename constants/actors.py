# To distinguish actor constants from character constants, a number is appended to
# the end, even if it's the only actor of that character. The index of the actor is
# relative to the order the actors would join you in vanilla.

def set_constants(main):
 if len(main.actors) > 0:
  main.DKCECIL1 = main.actors[1]
 if len(main.actors) > 1:
  main.KAIN1 =    main.actors[2]
 if len(main.actors) > 2:
  main.RYDIA1 =   main.actors[3]
 if len(main.actors) > 3:
  main.TELLAH1 =  main.actors[4]
 if len(main.actors) > 4:
  main.EDWARD1 =  main.actors[5]
 if len(main.actors) > 5:
  main.ROSA1 =    main.actors[6]
 if len(main.actors) > 6:
  main.YANG1 =    main.actors[7]
 if len(main.actors) > 7:
  main.PALOM1 =   main.actors[8]
 if len(main.actors) > 8:
  main.POROM1 =   main.actors[9]
 if len(main.actors) > 9:
  main.TELLAH2 =  main.actors[10]
 if len(main.actors) > 10:
  main.PALADINCECIL, main.CECIL = main.actors[11], main.actors[11]
 if len(main.actors) > 11:
  main.TELLAH3 =  main.actors[12]
 if len(main.actors) > 12:
  main.YANG2 =    main.actors[13]
 if len(main.actors) > 13:
  main.CID1 =     main.actors[14]
 if len(main.actors) > 14:
  main.KAIN2 =    main.actors[15]
 if len(main.actors) > 15:
  main.ROSA2 =    main.actors[16]
 if len(main.actors) > 16:
  main.RYDIA2 =   main.actors[17]
 if len(main.actors) > 17:
  main.EDGE1 =    main.actors[18]
 if len(main.actors) > 18:
  main.FUSOYA1 =  main.actors[19]
 if len(main.actors) > 19:
  main.KAIN3 =    main.actors[20]
