package com;

import com.twitter.TwitterController;

/**
 * 测试用,不用启动springboot
 */
public class TestWithNoSpring {
    public static void main(String[] args) {
        TwitterController t = new TwitterController();
        t.getUserDetail();
    }
}
