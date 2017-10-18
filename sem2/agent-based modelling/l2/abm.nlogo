to setup
  clear-all
  reset-ticks
  
  [
    ask patches 
    [ 
      ifelse random 100 < 70
      [
        set pcolor green 
      ]
      [
        set pcolor grey
      ]
    ]
  ]
end

to go
  ask turtles [
    fd 1            ;; forward 1 step
    rt random 100    ;; turn right
    lt random 100    ;; turn left
  ]
  tick
end
  
to draw-polygon [num-sides len]  ;; turtle procedure
  pen-down
  repeat num-sides [
    fd len
    rt 360 / num-sides
  ]
end
