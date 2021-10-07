package com.twitter;

import com.alibaba.fastjson.JSONObject;
import com.twitter.pojo.Tweet;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/Twitter")
public class TwitterController {

    @Autowired
    private TwitterService twitterService;

    //http://localhost:4567/Twitter/getUserDetail
    @GetMapping("/getUserDetail")
    public String getUserDetail() {
        //UserByScreenName?
//        String a = "{\"data\":{\"user\":{\"result\":{\"__typename\":\"User\",\"id\":\"VXNlcjo3NDQ5MDY5NTY2NDk4NTcwMjQ=\",\"rest_id\":\"744906956649857024\",\"affiliates_highlighted_label\":{},\"legacy\":{\"blocked_by\":false,\"blocking\":false,\"can_dm\":false,\"can_media_tag\":true,\"created_at\":\"Mon Jun 20 14:57:12 +0000 2016\",\"default_profile\":true,\"default_profile_image\":false,\"description\":\"「リーユウ」 中国上海人、歌·コスプレ、167cm、Ins：koi_liyuu、最新情報@LiyuuStaff 、FC「YuU Koi Days」、#俺100 ED「カルペ・ディエム」、「ラブライブ！スーパースター‼︎」Liella!唐 可可役、お仕事ご依頼liyuu.horiprointer@gmail.com\",\"entities\":{\"description\":{\"urls\":[]},\"url\":{\"urls\":[{\"display_url\":\"liyuu0109.com\",\"expanded_url\":\"https://liyuu0109.com/\",\"url\":\"https://t.co/KiKd8225vY\",\"indices\":[0,23]}]}},\"fast_followers_count\":0,\"favourites_count\":6460,\"follow_request_sent\":false,\"followed_by\":false,\"followers_count\":599890,\"following\":true,\"friends_count\":251,\"has_custom_timelines\":true,\"is_translator\":false,\"listed_count\":5248,\"location\":\"ホリプロインターナショナル所属\",\"media_count\":793,\"muting\":false,\"name\":\"Liyuu\",\"normal_followers_count\":599890,\"notifications\":false,\"pinned_tweet_ids_str\":[\"1338320110176518144\"],\"profile_banner_extensions\":{\"mediaColor\":{\"r\":{\"ok\":{\"palette\":[{\"percentage\":47.37,\"rgb\":{\"blue\":184,\"green\":178,\"red\":207}},{\"percentage\":27.02,\"rgb\":{\"blue\":136,\"green\":123,\"red\":193}},{\"percentage\":8.56,\"rgb\":{\"blue\":109,\"green\":83,\"red\":213}},{\"percentage\":7.78,\"rgb\":{\"blue\":159,\"green\":170,\"red\":221}},{\"percentage\":1.96,\"rgb\":{\"blue\":203,\"green\":194,\"red\":154}}]}}}},\"profile_banner_url\":\"https://pbs.twimg.com/profile_banners/744906956649857024/1557133498\",\"profile_image_extensions\":{\"mediaColor\":{\"r\":{\"ok\":{\"palette\":[{\"percentage\":56.06,\"rgb\":{\"blue\":131,\"green\":172,\"red\":197}},{\"percentage\":27.63,\"rgb\":{\"blue\":18,\"green\":36,\"red\":60}},{\"percentage\":4.71,\"rgb\":{\"blue\":143,\"green\":149,\"red\":155}},{\"percentage\":2.63,\"rgb\":{\"blue\":37,\"green\":71,\"red\":120}},{\"percentage\":1.13,\"rgb\":{\"blue\":6,\"green\":8,\"red\":18}}]}}}},\"profile_image_url_https\":\"https://pbs.twimg.com/profile_images/1345403314289033216/sSfHEpO0_normal.jpg\",\"profile_interstitial_type\":\"\",\"protected\":false,\"screen_name\":\"Liyu0109\",\"statuses_count\":1904,\"translator_type\":\"none\",\"url\":\"https://t.co/KiKd8225vY\",\"verified\":false,\"want_retweets\":true,\"withheld_in_countries\":[]},\"smart_blocked_by\":false,\"smart_blocking\":false,\"legacy_extended_profile\":{\"birthdate\":{\"day\":9,\"month\":1,\"visibility\":\"Public\",\"year_visibility\":\"Self\"}},\"is_profile_translatable\":true}}}}\n";
//        twitterService.analyzeUserDetailJSON(a);
        return "getUserDetail";
    }
    @GetMapping("/getUserTweets")
    public String getUserTweets(StringBuilder b) {//获取某用户推文
        //UserTweets?
        twitterService.analyzeUserTweetsJSON(b);
        return "getUserTweets";
    }
}
