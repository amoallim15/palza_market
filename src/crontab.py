import requests
import mysql.connector
# 
# example
# cursor.execute("UPDATE item SET is_finish = '%s' WHERE secret_hp = '%s'", 0, '614-21-60909')
# 
db_config = {
   "user": "palja",
   "password": "123456",
   "host": "localhost",
   "port": "3306" ,
   "database": "palja"
}
# 
url_config = {
    "url": "http://api.odcloud.kr/api/nts-businessman/v1/status",
    "serviceKey": "MgY51pDPRtCjEZlQz%2B2ZCiZvTnxEPoABjRFnRQXMcQtyaC3hwLF8P51nid7ghxIKhXxu7SAhqAfM7Snxmlj8hA%3D%3D",
    "returnType": "json" 
}
# 
business_status = ["01", "03"]
#
def batcher(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
# 
def cond(val):
    if val == "01":
        return 0
    else:
        return 1

def main():
    result = []
    # 
    # 1. connect to database.
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 2. get business nums.
    business_nums = {}
    cursor.execute("SELECT secret_hp FROM item WHERE secret_hp != '';")
    data = list(map(lambda x: { x[0].replace('-', ''): x[0] }, cursor.fetchall()))
    for n in data:
        business_nums.update(n)
    print(business_nums)

    # 3. build url.
    url = f"{url_config['url']}?serviceKey={url_config['serviceKey']}&returnType={url_config['returnType']}"
    print(url)
    # 

    # 4. get businesses status.
    for batch in batcher(list(business_nums.keys()), 10):
        # print(batch)
        res = requests.post(url, json={ "b_no": batch })
        res_json = res.json()
        if res_json["status_code"] == "OK":
            batch_result = list(map(lambda x: { "secret_hp": business_nums[x["b_no"]], "is_finish": cond(x["b_stt_cd"]) }, res_json["data"]))
            result += batch_result
            print(batch_result)
            # break
        # break

    print(result)
    # 5. execute sql update command
    for item in result:
        secret_hp = item["secret_hp"]
        is_finish = item["is_finish"]
        cursor.execute(f"UPDATE item SET is_finish = {is_finish} WHERE secret_hp = '{secret_hp}';")
    # 6. commit result
    conn.commit()

    # 7. exit code
    pass

if __name__ == "__main__":
    main()