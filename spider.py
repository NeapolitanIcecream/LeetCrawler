import requests
import json
import re

_topics = []
_posts = []
dataSize = 1500
solutionPattern = '.*?```(.*?)\n(.*?)```.*?'


def graphql(query):
    headers = {
        'authority':
        'leetcode-cn.com',
        'pragma':
        'no-cache',
        'cache-control':
        'no-cache',
        'accept':
        '*/*',
        'origin':
        'https://leetcode-cn.com',
        'x-csrftoken':
        'th5b5pvnyJi56VqpbE71jLyvN9zoYfiTt0SLpw19PzorKzvwTDx8BAkfhdk184Jc',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        'content-type':
        'application/json',
        'sec-fetch-site':
        'same-origin',
        'sec-fetch-mode':
        'cors',
        'referer':
        'https://leetcode-cn.com/problems/two-sum/solution/',
        'accept-encoding':
        'gzip, deflate, br',
        'accept-language':
        'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'cookie':
        'csrftoken=th5b5pvnyJi56VqpbE71jLyvN9zoYfiTt0SLpw19PzorKzvwTDx8BAkfhdk184Jc; Hm_lvt_fa218a3ff7179639febdb15e372f411c=1572938196; _ga=GA1.2.857435596.1572938196; _gid=GA1.2.1950373803.1572938196; _gat_gtag_UA_131851415_1=1; gr_user_id=e7a9b1a4-4b4b-45a1-bfbf-38c6efe6149e; a2873925c34ecbd2_gr_session_id=0a19a3e6-bf66-43a1-a3a0-dceb6bde329a; grwng_uid=3ecec8fd-b0f6-4e5f-a6b6-dfdebab505fc; a2873925c34ecbd2_gr_session_id_0a19a3e6-bf66-43a1-a3a0-dceb6bde329a=true; __asc=9a2e95b316e3a6c34d08472293b; __auc=9a2e95b316e3a6c34d08472293b; Hm_lpvt_fa218a3ff7179639febdb15e372f411c=1572938201',
    }

    data = json.dumps(query)
    response = requests.post('https://leetcode-cn.com/graphql/',
                             headers=headers,
                             data=data)
    return json.loads(response.text)


def getAllQuetions():
    query = {
        "operationName":
        "allQuestions",
        "variables": {},
        "query":
        "query allQuestions {\n  allQuestionsBeta {\n    ...questionSummaryFields\n    __typename\n  }\n}\n\nfragment questionSummaryFields on QuestionNode {\n  title\n  titleSlug\n  translatedTitle\n  questionId\n  questionFrontendId\n  status\n  difficulty\n  isPaidOnly\n  categoryTitle\n  __typename\n}\n"
    }

    return graphql(query)


def getQuetion(titleSlug):
    query = {
        "operationName":
        "questionData",
        "variables": {
            "titleSlug": titleSlug
        },
        "query":
        "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    book {\n      id\n      bookName\n      pressName\n      description\n      bookImgUrl\n      pressImgUrl\n      productUrl\n      __typename\n    }\n    isSubscribed\n    __typename\n  }\n}\n"
    }

    return graphql(query)


def getComments(topicId):
    query = {
        "operationName":
        "commonTopicComments",
        "variables": {
            "topicId": 2,
            "skip": 0,
            "orderBy": "HOT"
        },
        "query":
        "query commonTopicComments($topicId: Int!, $orderBy: CommentOrderBy, $skip: Int) {\n  commonTopicComments(topicId: $topicId, orderBy: $orderBy, skip: $skip, first: 15) {\n    totalNum\n    edges {\n      node {\n        ...commentFields\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment commentFields on CommentRelayNode {\n  id\n  numChildren\n  isEdited\n  post {\n    id\n    content\n    voteUpCount\n    creationDate\n    updationDate\n    status\n    voteStatus\n    author {\n      username\n      isDiscussAdmin\n      profile {\n        userSlug\n        userAvatar\n        realName\n        __typename\n      }\n      __typename\n    }\n    mentionedUsers {\n      key\n      username\n      userSlug\n      nickName\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
    }

    return graphql(query)


def getReply(commentId):
    query = {
        "operationName":
        "commentReplyConnection",
        "variables": {
            "commentId": commentId,
            "orderBy": "OLD_TO_NEW",
            "first": 10,
            "skip": 0
        },
        "query":
        "query commentReplyConnection($commentId: ID!, $orderBy: CommentReplyOrderBy, $skip: Int, $first: Int) {\n  commentReplyConnection(commentId: $commentId, orderBy: $orderBy, skip: $skip, first: $first) {\n    totalNum\n    edges {\n      node {\n        ...commentFields\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment commentFields on CommentRelayNode {\n  id\n  numChildren\n  isEdited\n  post {\n    id\n    content\n    voteUpCount\n    creationDate\n    updationDate\n    status\n    voteStatus\n    author {\n      username\n      isDiscussAdmin\n      profile {\n        userSlug\n        userAvatar\n        realName\n        __typename\n      }\n      __typename\n    }\n    mentionedUsers {\n      key\n      username\n      userSlug\n      nickName\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
    }

    return graphql(query)


def getSolution(content):
    solution = {}

    matchObj = re.match(solutionPattern, content, re.M | re.U | re.S)

    if matchObj:
        solution['language'] = matchObj.group(1)
        solution['code'] = matchObj.group(2)

    return solution


def solution():
    allQuestions = getAllQuetions()

    cnt1 = 0  # Debug: question cnt

    for allQuestionsItr in allQuestions['data']['allQuestionsBeta']:
        if cnt1 < dataSize:
            cnt1 += 1
        else:
            break

        if allQuestionsItr['isPaidOnly']:
            continue

        questionId = allQuestionsItr['questionId']

        title = allQuestionsItr['title']

        titleSlug = allQuestionsItr['titleSlug']

        question = getQuetion(titleSlug)['data']['question']

        boundTopicId = question['boundTopicId']

        topicId = boundTopicId

        topics = getComments(topicId)

        cnt2 = 0  # Debug: topic cnt

        for topicsItr in topics['data']['commonTopicComments']['edges']:
            if cnt2 < dataSize:
                cnt2 += 1
            else:
                break

            global _topics
            global _posts
            topicAppend = {}
            postAppend = {}

            node = topicsItr['node']

            commentId = node['id']

            post = node['post']
            postId = post['id']
            realName = post['author']['profile']['realName']
            content = post['content']

            topicAppend['questionId'] = questionId
            topicAppend['topicId'] = topicId
            topicAppend['title'] = title
            topicAppend['post'] = postId

            _topics.append(topicAppend)

            postAppend['parent'] = -1
            postAppend['id'] = postId
            postAppend['content'] = content
            postAppend['voteCount'] = post['voteUpCount']
            postAppend['creationDate'] = post['creationDate']
            postAppend['updationDate'] = post['updationDate']
            postAppend['author'] = realName
            postAppend['solution'] = getSolution(content)

            _posts.append(postAppend)

            replies = getReply(commentId)

            cnt3 = 0

            for repliesItr in replies['data']['commentReplyConnection']['edges']:
                if cnt3 < dataSize:
                    cnt3 += 1
                else:
                    break

                postAppend = {}

                replyNode = repliesItr['node']

                replyPost = replyNode['post']

                replyRealName = replyPost['author']['profile']['realName']

                postAppend['parent'] = postId
                postAppend['id'] = replyPost['id']
                postAppend['content'] = replyPost['content']
                postAppend['voteCount'] = replyPost['voteUpCount']
                postAppend['creationDate'] = replyPost['creationDate']
                postAppend['updationDate'] = replyPost['updationDate']
                postAppend['author'] = replyRealName

                _posts.append(postAppend)


def main():
    solution()

    print(_topics)

    print(_posts)


if __name__ == "__main__":
    main()
