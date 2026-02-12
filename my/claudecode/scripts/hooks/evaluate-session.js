#!/usr/bin/env node
/**
 * 持续学习 - 会话评估器
 *
 * 跨平台支持 (Windows, macOS, Linux)
 *
 * 在 Stop hook 中运行，从 Claude Code 会话中提取可复用的模式
 *
 * 为什么使用 Stop hook 而非 UserPromptSubmit：
 * - Stop 在会话结束时运行一次（轻量）
 * - UserPromptSubmit 每条消息都运行（重量，增加延迟）
 */

const path = require('path');
const fs = require('fs');
const {
  getLearnedSkillsDir,
  ensureDir,
  readFile,
  countInFile,
  log
} = require('../lib/utils');

async function main() {
  // 获取脚本目录以查找配置文件
  const scriptDir = __dirname;
  const configFile = path.join(scriptDir, '..', '..', 'skills', 'continuous-learning', 'config.json');

  // 默认配置
  let minSessionLength = 10;
  let learnedSkillsPath = getLearnedSkillsDir();

  // 如果配置存在则加载
  const configContent = readFile(configFile);
  if (configContent) {
    try {
      const config = JSON.parse(configContent);
      minSessionLength = config.min_session_length || 10;

      if (config.learned_skills_path) {
        // 处理路径中的 ~
        learnedSkillsPath = config.learned_skills_path.replace(/^~/, require('os').homedir());
      }
    } catch {
      // 配置无效，使用默认值
    }
  }

  // 确保 learned skills 目录存在
  ensureDir(learnedSkillsPath);

  // 从环境变量获取会话记录路径（由 Claude Code 设置）
  const transcriptPath = process.env.CLAUDE_TRANSCRIPT_PATH;

  if (!transcriptPath || !fs.existsSync(transcriptPath)) {
    process.exit(0);
  }

  // 统计会话中的用户消息数量
  const messageCount = countInFile(transcriptPath, /"type":"user"/g);

  // 跳过短会话
  if (messageCount < minSessionLength) {
    log(`[ContinuousLearning] 会话过短 (${messageCount} 条消息)，跳过评估`);
    process.exit(0);
  }

  // 提示 Claude 该会话应评估是否有可提取的模式
  log(`[ContinuousLearning] 会话包含 ${messageCount} 条消息 - 评估可提取的模式`);
  log(`[ContinuousLearning] 保存 learned skills 到: ${learnedSkillsPath}`);

  process.exit(0);
}

main().catch(err => {
  console.error('[ContinuousLearning] 错误:', err.message);
  process.exit(0);
});
