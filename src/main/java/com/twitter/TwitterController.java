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
//        twitterService.AnalyzeUserDetailJSON(a);
        return "getUserDetail";
    }
    @GetMapping("/getUserTweets")
    public String getUserTweets(StringBuilder b) {//获取某用户推文
        //UserTweets?
        JSONObject json = JSONObject.parseObject(b.toString());
        JSONObject timelineJson = json.getJSONObject("data")
                .getJSONObject("user")
                .getJSONObject("result")
                .getJSONObject("timeline")
                .getJSONObject("timeline")
                ;
        List<JSONObject> instructionsList = (List<JSONObject>) timelineJson.get("instructions");
        List<Tweet> tweets = new ArrayList<>();//提取完成后的推文数组
        for (JSONObject d : instructionsList) {
            //所有的推文,instructionsList的下一组是置顶推文(TimelinePinEntry),现在暂时不理
            if ("TimelineAddEntries".equals(d.get("type"))) {
                List<JSONObject> entriesList = (List<JSONObject>) d.get("entries");
                for (JSONObject dd : entriesList) {
                    String entryId = dd.getString("entryId");
                    if (entryId.matches("^tweet-[0-9]*")) { //确认为用户推文
                        Tweet tweet = new Tweet();
                        JSONObject itemContent = dd.getJSONObject("content").getJSONObject("itemContent");
                        tweet.setTweet_display_type(itemContent.getString("tweetDisplayType"));
                        JSONObject result = itemContent.getJSONObject("tweet_results").getJSONObject("result");
                        String username = result.getJSONObject("core")
                                .getJSONObject("user_results")
                                .getJSONObject("result")
                                .getJSONObject("legacy")
                                .getString("screen_name");
                        tweet.setUsername(username);

                        String id = result.getJSONObject("core")
                                .getJSONObject("user_results")
                                .getJSONObject("result")
                                .getString("id");
                        tweet.setUser_id(id);

                        JSONObject legacy = result.getJSONObject("legacy");
                        tweet.setTweet_id(legacy.getString("id_str"));
                        tweet.setFull_text(legacy.getString("full_text"));
                        tweet.setCreated_at(legacy.getString("created_at"));

                        if (legacy.getBoolean("is_quote_status")) {
                            tweet.setQuoted_tweet_id(legacy.getString("quoted_status_id_str"));
                            JSONObject quotedResult = result.getJSONObject("quoted_status_result").getJSONObject("result");
                            //todo 完成转推的内容

                            tweets.add(tweet);
                        } else if (entryId.matches("^homeConversation-[0-9-a-zA-Z]*")) { //连续推文
                            System.out.println("连续推文");
                        } else if (entryId.matches("^promotedTweet-[0-9-a-zA-Z]*")) { //推广推文(广告)
//                        System.out.println("推广推文,暂时不处理");
                        } else if (entryId.matches("^whoToFollow-[0-9-a-zA-Z]*")) { //推荐关注
//                        System.out.println("推荐关注,暂时不处理");
                        } else if (entryId.matches("^cursor-top-[0-9-a-zA-Z]*")) { //光标顶部
//                        System.out.println("光标顶部,暂时不处理");
                        } else if (entryId.matches("^cursor-bottom-[0-9-a-zA-Z]*")) { //光标底部
//                        System.out.println("光标底部,暂时不处理");
                        }
                    }
                }
            }else if ("TimelinePinEntry".equals(d.get("type"))){//置顶推文
//                System.out.println("TimelinePinEntry,暂时不处理");
            }
        }
        return "getUserTweets";
    }
}
