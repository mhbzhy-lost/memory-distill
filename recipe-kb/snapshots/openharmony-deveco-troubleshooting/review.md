# 快照人审：openharmony-deveco-troubleshooting

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/common_problem_of_application.md
- 最终 URL: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/common_problem_of_application.md
- 来源类型: official_doc
- 采集时间: 2026-05-26T12:26:11.870151Z
- HTTP 状态: 200
- 内容哈希: sha256:896f52990f0bd55431db2f1fac18caf1d754ad1fa67825ae53dd0ba1c1f6851b
- 技术栈: harmonyos, arkts
- 抽取段落数: 9

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 9
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 3/5 条 expected_failure_hints

## 预期线索命中
- `appIdentifier 应用唯一标识`
  - [openharmony-deveco-troubleshooting-4] ## 什么是appIdentifier appIdentifier是<!--RP1-->[Profile签名文件](../security/app-provision-structure.md)<!--RP1End-->中的一个字段，为应用的唯一标识，在应用签名时生成，其中： 1. 通过DevEco Studio工具[自动签名](https://developer.huawei.com/consumer/cn/doc/harmon...
  - [openharmony-deveco-troubleshooting-5] ## 如何获取应用信息中的appIdentifier * 可以调用[bundleManager.getBundleInfoForSelf](../reference/apis-ability-kit/js-apis-bundleManager.md#bundlemanagergetbundleinfoforself)获取自身的BundleInfo应用包信息，应用包信息中包含signatureInfo签名信息，签名信息中包含appI...
  - [openharmony-deveco-troubleshooting-6] # 需将com.example.myapplication替换为实际应用的包名 bm dump -n com.example.myapplication | grep appIdentifier ``` ![alt text](figures/get_appIdentifier.png)
- `appId 应用唯一标识`：未找到直接段落命中
- `bundleManager getBundleInfoForSelf`
  - [openharmony-deveco-troubleshooting-2] ## 如何获取签名信息中的指纹信息 * 通过调用接口获取。 可以调用[bundleManager.getBundleInfoForSelf](../reference/apis-ability-kit/js-apis-bundleManager.md#bundlemanagergetbundleinfoforself)获取自身的BundleInfo应用包信息，应用包信息中包含signatureInfo签名信息，签名信息中包含fin...
  - [openharmony-deveco-troubleshooting-5] ## 如何获取应用信息中的appIdentifier * 可以调用[bundleManager.getBundleInfoForSelf](../reference/apis-ability-kit/js-apis-bundleManager.md#bundlemanagergetbundleinfoforself)获取自身的BundleInfo应用包信息，应用包信息中包含signatureInfo签名信息，签名信息中包含appI...
  - [openharmony-deveco-troubleshooting-8] ## 如何获取应用信息中的appId * 可以调用[bundleManager.getBundleInfoForSelf](../reference/apis-ability-kit/js-apis-bundleManager.md#bundlemanagergetbundleinfoforself)获取自身的BundleInfo应用包信息，应用包信息中包含signatureInfo签名信息，签名信息中包含appId信息。 <!-...
- `signatureInfo 签名信息`
  - [openharmony-deveco-troubleshooting-2] ## 如何获取签名信息中的指纹信息 * 通过调用接口获取。 可以调用[bundleManager.getBundleInfoForSelf](../reference/apis-ability-kit/js-apis-bundleManager.md#bundlemanagergetbundleinfoforself)获取自身的BundleInfo应用包信息，应用包信息中包含signatureInfo签名信息，签名信息中包含fin...
  - [openharmony-deveco-troubleshooting-5] ## 如何获取应用信息中的appIdentifier * 可以调用[bundleManager.getBundleInfoForSelf](../reference/apis-ability-kit/js-apis-bundleManager.md#bundlemanagergetbundleinfoforself)获取自身的BundleInfo应用包信息，应用包信息中包含signatureInfo签名信息，签名信息中包含appI...
  - [openharmony-deveco-troubleshooting-8] ## 如何获取应用信息中的appId * 可以调用[bundleManager.getBundleInfoForSelf](../reference/apis-ability-kit/js-apis-bundleManager.md#bundlemanagergetbundleinfoforself)获取自身的BundleInfo应用包信息，应用包信息中包含signatureInfo签名信息，签名信息中包含appId信息。 <!-...
- `fingerprint 指纹信息`：未找到直接段落命中

## 段落样例
- [openharmony-deveco-troubleshooting-1] # 应用程序包常见问题 <!--Kit: Ability Kit--> <!--Subsystem: BundleManager--> <!--Owner: @wanghang904--> <!--Designer: @hanfeng6--> <!--Tester: @kongjing2--> <!--Adviser: @Brilliantry_Rui-->
- [openharmony-deveco-troubleshooting-2] ## 如何获取签名信息中的指纹信息 * 通过调用接口获取。 可以调用[bundleManager.getBundleInfoForSelf](../reference/apis-ability-kit/js-apis-bundleManager.md#bundlemanagergetbundleinfoforself)获取自身的BundleInfo应用包信息，应用包信息中包含signatureInfo签名信息，签名信息中包含fin...
- [openharmony-deveco-troubleshooting-3] # 需将com.example.myapplication替换为实际应用的包名 bm dump -n com.example.myapplication | grep fingerprint ``` ![alt text](figures/get_fingerprint.png) * 通过.cer证书文件获取，可以参考[APP备案FAQ](https://developer.huawei.com/consumer/cn/doc/a...
- [openharmony-deveco-troubleshooting-4] ## 什么是appIdentifier appIdentifier是<!--RP1-->[Profile签名文件](../security/app-provision-structure.md)<!--RP1End-->中的一个字段，为应用的唯一标识，在应用签名时生成，其中： 1. 通过DevEco Studio工具[自动签名](https://developer.huawei.com/consumer/cn/doc/harmon...
- [openharmony-deveco-troubleshooting-5] ## 如何获取应用信息中的appIdentifier * 可以调用[bundleManager.getBundleInfoForSelf](../reference/apis-ability-kit/js-apis-bundleManager.md#bundlemanagergetbundleinfoforself)获取自身的BundleInfo应用包信息，应用包信息中包含signatureInfo签名信息，签名信息中包含appI...
- [openharmony-deveco-troubleshooting-6] # 需将com.example.myapplication替换为实际应用的包名 bm dump -n com.example.myapplication | grep appIdentifier ``` ![alt text](figures/get_appIdentifier.png)
- [openharmony-deveco-troubleshooting-7] ## 什么是appId appId是应用的唯一标识，由包名、下划线和证书公钥的Base64编码组成。由于appId和签名信息相关，如果签名证书的公钥更换，appId也会跟随变化，所以应用的唯一标识推荐使用[appIdentifier](#什么是appidentifier)。
- [openharmony-deveco-troubleshooting-8] ## 如何获取应用信息中的appId * 可以调用[bundleManager.getBundleInfoForSelf](../reference/apis-ability-kit/js-apis-bundleManager.md#bundlemanagergetbundleinfoforself)获取自身的BundleInfo应用包信息，应用包信息中包含signatureInfo签名信息，签名信息中包含appId信息。 <!-...

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
