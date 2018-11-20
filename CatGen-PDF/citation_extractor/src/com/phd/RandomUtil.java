package com.phd;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;


public class RandomUtil {


    private static final RandomUtil instance = new RandomUtil();
    public static RandomUtil getInstance() {
        return instance;
    }

    private Map<String, Integer> map = new HashMap<String, Integer>();


    public Integer generateRandom(Integer size) {

        Random rand = new Random();
        int index = rand.nextInt(size) + 0;

        while (isExist(index)) {
            index = rand.nextInt(size) + 0;
        }

        addRandom(index);
        return index;
    }

    private Boolean isExist(Integer num) {
        return  map.containsKey(num.toString());
    }

    public void clearExistedRandomList() {
        map.clear();
    }

    public void addRandom(Integer num) {
        map.put(num.toString(), num);
    }

}