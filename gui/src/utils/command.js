export function joinPostSyncCommands(filePath, title, digest, category, cover, topic, sites, tags, columns) {
  /**
 * 拼接 PostSync 命令行参数
 *
 * @param filePath 文件路径
 * @param title 标题
 * @param digest 摘要
 * @param category 分类
 * @param cover 封面
 * @param topic 话题
 * @param sites 站点列表
 * @param tags 标签列表
 * @param columns 专栏列表
 * @returns 拼接后的 PostSync 命令行参数
 * @throws 当 filePath 或 title 为空时，抛出错误
 */
  let command = 'bin\\PostSync.exe -f '
  if (filePath === undefined || filePath == '') {
    throw new Error('filePath is required')
  }
  if (title === undefined || title == '') {
    throw new Error('title is required')
  }
  if (digest.trim() != '') {
    digest = ` -f ${digest} `
  }
  if (category.trim() != '') {
    category = ` --category ${category} `
  }
  if (cover.trim() != '') {
    cover = ` --cover ${cover} `
  }
  if (topic.trim() != '') {
    topic = ` --topic ${topic} `
  }
  if (sites.length != 0) {
    sites = ` --site ${sites.join(' ')} `
  }
  if (tags.length != 0) {
    tags = ` --tag ${tags.join(' ')} `
  }
  if (columns.length != 0) {
    columns = ` --column ${columns.join(' ')} `
  }
  return command + filePath + digest + category + cover + topic + sites + tags + columns
}