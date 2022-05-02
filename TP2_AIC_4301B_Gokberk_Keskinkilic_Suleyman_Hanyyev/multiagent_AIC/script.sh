
# As far as i see, the hardest one to play, compile separately
# s=("trickyClassic") 


s=("capsuleClassic" "minimaxClassic" "powerClassis" "trappedClassic"
"contestClassic" "mediumClassic" "openClassic" "smallClassic" "originalClassic"
"testClassic")


# Just for reference
# capsuleClassic.lay   minimaxClassic.lay   powerClassic.lay     trappedClassic.lay
# contestClassic.lay   openClassic.lay      smallClassic.lay     trickyClassic.lay
# mediumClassic.lay    originalClassic.lay  testClassic.lay

### Open Classic Layout

for n in ${s[@]};
do
    echo $n

    echo " -------------1 GHOST + RANDOM-----------------"
    echo "\n"
    python3 pacman_AIC.py -p ReflexAgent -k 1 -l $n -n 100 -q

    echo "--------------1 GHOST + FIXED SEED-------------"
    echo "\n"
    python3 pacman_AIC.py -p ReflexAgent -k 1 -l $n -n 100 -q -f
    
    echo "--------------1 GHOST + DIRECTIONALGHOST-------"
    echo "\n"
    python3 pacman_AIC.py -p ReflexAgent -k 1 -l $n -n 100 -q -g DirectionalGhost
    
    echo "--------------2 GHOSTS + RANDOM----------------"
    echo "\n"
    python3 pacman_AIC.py -p ReflexAgent -k 2 -l $n -n 100 -q
    
    echo "--------------2 GHOSTS + FIXED SEED------------"
    echo "\n"
    python3 pacman_AIC.py -p ReflexAgent -k 2 -l $n -n 100 -q -f

    echo "--------------2 GHOSTS+ DIRECTIONALGHOST------"
    echo "\n"
    python3 pacman_AIC.py -p ReflexAgent -k 2 -l $n -n 100 -q -g DirectionalGhost
    
done
