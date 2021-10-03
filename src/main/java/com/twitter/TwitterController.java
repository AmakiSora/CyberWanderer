package com.twitter;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.twitter.twitterDataDao.TwitterDataDao;
import com.twitter.pojo.TwitterUser;
import org.jasypt.encryption.StringEncryptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/Twitter")
public class TwitterController {
    @Autowired
    StringEncryptor encryptor;

    @Autowired
    private TwitterDataDao twitterDataDao;
    //http://localhost:4567/Twitter/getUserDetail
    @GetMapping("/getUserDetail")
    public String getUserDetail(){
        String a = "{\"data\":{\"user\":{\"result\":{\"__typename\":\"User\",\"id\":\"VXNlcjoxNTY1NjM1OTc=\",\"rest_id\":\"156563597\",\"affiliates_highlighted_label\":{},\"legacy\":{\"blocked_by\":false,\"blocking\":false,\"can_dm\":true,\"can_media_tag\":true,\"created_at\":\"Thu Jun 17 07:54:48 +0000 2010\",\"default_profile\":false,\"default_profile_image\":false,\"description\":\"Artist ■1st フルAL「OVERTONES」7/7 Release 予約受付中 https://t.co/VHEXZts2xU ■ Instagram https://t.co/Syfq8HAnrG ■お仕事お問合わせ UUUM株式会社まで\",\"entities\":{\"description\":{\"urls\":[{\"display_url\":\"uuum.jp/posts/312133\",\"expanded_url\":\"https://uuum.jp/posts/312133\",\"url\":\"https://t.co/VHEXZts2xU\",\"indices\":[45,68]},{\"display_url\":\"instagram.com/keibamboo/?hl=…\",\"expanded_url\":\"https://www.instagram.com/keibamboo/?hl=ja\",\"url\":\"https://t.co/Syfq8HAnrG\",\"indices\":[81,104]}]},\"url\":{\"urls\":[{\"display_url\":\"youtu.be/y9ltZL5osBI\",\"expanded_url\":\"https://youtu.be/y9ltZL5osBI\",\"url\":\"https://t.co/QYJWJwgTp4\",\"indices\":[0,23]}]}},\"fast_followers_count\":0,\"favourites_count\":1247,\"follow_request_sent\":false,\"followed_by\":false,\"followers_count\":153041,\"following\":true,\"friends_count\":536,\"has_custom_timelines\":true,\"is_translator\":false,\"listed_count\":1343,\"location\":\"AB型 Tokyo → LA → Tokyo\",\"media_count\":1253,\"muting\":false,\"name\":\"竹渕慶 | Kei Takebuchi\",\"normal_followers_count\":153041,\"notifications\":false,\"pinned_tweet_ids_str\":[\"1423661408839868423\"],\"profile_banner_extensions\":{\"mediaColor\":{\"r\":{\"ok\":{\"palette\":[{\"percentage\":55.36,\"rgb\":{\"blue\":181,\"green\":188,\"red\":132}},{\"percentage\":24.84,\"rgb\":{\"blue\":195,\"green\":158,\"red\":196}},{\"percentage\":16.9,\"rgb\":{\"blue\":202,\"green\":178,\"red\":144}},{\"percentage\":4.14,\"rgb\":{\"blue\":183,\"green\":149,\"red\":219}},{\"percentage\":3.56,\"rgb\":{\"blue\":192,\"green\":189,\"red\":189}}]}}}},\"profile_banner_url\":\"https://pbs.twimg.com/profile_banners/156563597/1621596793\",\"profile_image_extensions\":{\"mediaColor\":{\"r\":{\"ok\":{\"palette\":[{\"percentage\":41.04,\"rgb\":{\"blue\":121,\"green\":101,\"red\":115}},{\"percentage\":30.49,\"rgb\":{\"blue\":114,\"green\":108,\"red\":166}},{\"percentage\":9.28,\"rgb\":{\"blue\":16,\"green\":23,\"red\":23}},{\"percentage\":5.56,\"rgb\":{\"blue\":178,\"green\":195,\"red\":239}},{\"percentage\":4.4,\"rgb\":{\"blue\":75,\"green\":89,\"red\":167}}]}}}},\"profile_image_url_https\":\"https://pbs.twimg.com/profile_images/1395700507893587978/UHy1tdLk_normal.jpg\",\"profile_interstitial_type\":\"\",\"protected\":false,\"screen_name\":\"keibambooty\",\"statuses_count\":10042,\"translator_type\":\"none\",\"url\":\"https://t.co/QYJWJwgTp4\",\"verified\":true,\"want_retweets\":true,\"withheld_in_countries\":[]},\"smart_blocked_by\":false,\"smart_blocking\":false,\"legacy_extended_profile\":{\"birthdate\":{\"day\":11,\"month\":7,\"year\":1991,\"visibility\":\"Public\",\"year_visibility\":\"Public\"}},\"is_profile_translatable\":false}}}}";
//        String a = "{\"data\":{\"user\":{\"result\":{\"__typename\":\"User\",\"id\":\"VXNlcjo3NDQ5MDY5NTY2NDk4NTcwMjQ=\",\"rest_id\":\"744906956649857024\",\"affiliates_highlighted_label\":{},\"legacy\":{\"blocked_by\":false,\"blocking\":false,\"can_dm\":false,\"can_media_tag\":true,\"created_at\":\"Mon Jun 20 14:57:12 +0000 2016\",\"default_profile\":true,\"default_profile_image\":false,\"description\":\"「リーユウ」 中国上海人、歌·コスプレ、167cm、Ins：koi_liyuu、最新情報@LiyuuStaff 、FC「YuU Koi Days」、#俺100 ED「カルペ・ディエム」、「ラブライブ！スーパースター‼︎」Liella!唐 可可役、お仕事ご依頼liyuu.horiprointer@gmail.com\",\"entities\":{\"description\":{\"urls\":[]},\"url\":{\"urls\":[{\"display_url\":\"liyuu0109.com\",\"expanded_url\":\"https://liyuu0109.com/\",\"url\":\"https://t.co/KiKd8225vY\",\"indices\":[0,23]}]}},\"fast_followers_count\":0,\"favourites_count\":6460,\"follow_request_sent\":false,\"followed_by\":false,\"followers_count\":599890,\"following\":true,\"friends_count\":251,\"has_custom_timelines\":true,\"is_translator\":false,\"listed_count\":5248,\"location\":\"ホリプロインターナショナル所属\",\"media_count\":793,\"muting\":false,\"name\":\"Liyuu\",\"normal_followers_count\":599890,\"notifications\":false,\"pinned_tweet_ids_str\":[\"1338320110176518144\"],\"profile_banner_extensions\":{\"mediaColor\":{\"r\":{\"ok\":{\"palette\":[{\"percentage\":47.37,\"rgb\":{\"blue\":184,\"green\":178,\"red\":207}},{\"percentage\":27.02,\"rgb\":{\"blue\":136,\"green\":123,\"red\":193}},{\"percentage\":8.56,\"rgb\":{\"blue\":109,\"green\":83,\"red\":213}},{\"percentage\":7.78,\"rgb\":{\"blue\":159,\"green\":170,\"red\":221}},{\"percentage\":1.96,\"rgb\":{\"blue\":203,\"green\":194,\"red\":154}}]}}}},\"profile_banner_url\":\"https://pbs.twimg.com/profile_banners/744906956649857024/1557133498\",\"profile_image_extensions\":{\"mediaColor\":{\"r\":{\"ok\":{\"palette\":[{\"percentage\":56.06,\"rgb\":{\"blue\":131,\"green\":172,\"red\":197}},{\"percentage\":27.63,\"rgb\":{\"blue\":18,\"green\":36,\"red\":60}},{\"percentage\":4.71,\"rgb\":{\"blue\":143,\"green\":149,\"red\":155}},{\"percentage\":2.63,\"rgb\":{\"blue\":37,\"green\":71,\"red\":120}},{\"percentage\":1.13,\"rgb\":{\"blue\":6,\"green\":8,\"red\":18}}]}}}},\"profile_image_url_https\":\"https://pbs.twimg.com/profile_images/1345403314289033216/sSfHEpO0_normal.jpg\",\"profile_interstitial_type\":\"\",\"protected\":false,\"screen_name\":\"Liyu0109\",\"statuses_count\":1904,\"translator_type\":\"none\",\"url\":\"https://t.co/KiKd8225vY\",\"verified\":false,\"want_retweets\":true,\"withheld_in_countries\":[]},\"smart_blocked_by\":false,\"smart_blocking\":false,\"legacy_extended_profile\":{\"birthdate\":{\"day\":9,\"month\":1,\"visibility\":\"Public\",\"year_visibility\":\"Self\"}},\"is_profile_translatable\":true}}}}\n";
        JSONObject Json = (JSONObject) JSON.parse(a);
        JSONObject userJson = (JSONObject) Json.getJSONObject("data").get("user");
        JSONObject resultJson = (JSONObject) userJson.getJSONObject("result");
        JSONObject legacy_extended_profileJson = (JSONObject) resultJson.getJSONObject("legacy_extended_profile");
        JSONObject legacyJson = (JSONObject) resultJson.getJSONObject("legacy");
        JSONObject birthdateJson = (JSONObject) legacy_extended_profileJson.getJSONObject("birthdate");

        String birthdate = birthdateJson.getString("year")+"-"+
                birthdateJson.getString("month")+"-"+
                birthdateJson.getString("day");

        TwitterUser user = new TwitterUser();
        user.setName(legacyJson.getString("name"));
        user.setUsername(legacyJson.getString("screen_name"));
        user.setCreated_at(legacyJson.getString("created_at"));
        user.setBirthday(birthdate);
        user.setDescription(legacyJson.getString("description"));
        user.setDisplay_url(legacyJson.getString("url"));
        user.setLocation(legacyJson.getString("location"));
        user.setFollowers_count(legacyJson.getInteger("followers_count"));
        user.setFriends_count(legacyJson.getInteger("friends_count"));

        twitterDataDao.insertTwitterUser(user);

        return "成功";
    }

}
