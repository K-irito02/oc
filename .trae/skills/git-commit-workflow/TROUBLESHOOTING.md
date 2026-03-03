# Git 提交工作流故障排除

本文件提供 Git 提交工作流的故障排除指南，帮助您解决在使用 Git 提交工作流时遇到的常见问题。

## 1. 环境状态仓库问题

### 1.1 GitHub Push Protection 拒绝

**症状：**
- 推送被拒绝，出现 "GH013: Repository rule violations found" 错误
- 提示 "Push cannot contain secrets"

**可能原因：**
- 提交中包含敏感信息，如 API 密钥、令牌、密码等
- 配置文件中包含硬编码的敏感信息
- 记忆文件中包含敏感数据

**解决方案：**
1. **撤销提交但保留更改**：
   ```powershell
   git reset --soft HEAD~1
   ```

2. **修改文件移除敏感信息**：
   - 检查并修改包含敏感信息的文件
   - 使用环境变量或配置文件管理敏感信息

3. **重新添加和提交**：
   ```powershell
   git add .
   git commit -m "config: 提交描述"
   git push origin main
   ```

4. **预防措施**：
   - 使用 .gitignore 排除包含敏感信息的文件
   - 配置预提交钩子检查敏感信息
   - 使用环境变量存储敏感配置

### 1.2 推送被拒绝（远程有更新）

**症状：**
- 推送被拒绝，出现 "non-fast-forward" 错误
- 提示 "remote contains work that you do not have locally"

**可能原因：**
- 远程仓库有其他开发者的提交
- 本地分支落后于远程分支

**解决方案：**
1. **拉取远程更新后重新推送**：
   ```powershell
   git pull origin main --rebase
   git push origin main
   ```

2. **强制推送（谨慎使用）**：
   ```powershell
   git push origin main --force-with-lease
   ```

### 1.3 文件过大

**症状：**
- 推送被拒绝，出现 "large file detected" 错误
- 提示 "remote: error: File <file> is XXX MB; this exceeds GitHub's file size limit of 100.00 MB"

**可能原因：**
- 提交了超过 GitHub 文件大小限制的文件
- 大文件未被 .gitignore 排除

**解决方案：**
1. **检查大文件**：
   ```powershell
   git ls-files --other --ignored --exclude-standard | head -20
   ```

2. **从提交历史中移除大文件**：
   ```powershell
   git filter-branch --force --index-filter "git rm --cached --ignore-unmatch <file>" --prune-empty --tag-name-filter cat -- --all
   git push origin main --force
   ```

3. **更新 .gitignore**：
   - 在 .gitignore 中添加大文件或目录
   - 例如：`*.exe`, `*.zip`, `node_modules/`

### 1.4 认证失败

**症状：**
- 推送时出现认证错误
- 提示 "remote: Invalid username or password"

**可能原因：**
- GitHub 密码已更改
- 个人访问令牌 (PAT) 已过期
- 认证配置错误

**解决方案：**
1. **重新配置认证**：
   ```powershell
   git config --global credential.helper store
   git push origin main
   # 输入用户名和新的个人访问令牌
   ```

2. **检查远程仓库配置**：
   ```powershell
   git remote -v
   # 确保远程仓库 URL 正确
   ```

3. **生成新的个人访问令牌**：
   - 登录 GitHub -> Settings -> Developer settings -> Personal access tokens
   - 生成新的令牌，选择适当的权限

## 2. 项目代码仓库问题

### 2.1 合并冲突

**症状：**
- 合并分支时出现冲突
- 提示 "CONFLICT (content): Merge conflict in <file>"

**可能原因：**
- 两个分支修改了同一个文件的相同部分
- 远程分支和本地分支有冲突的更改

**解决方案：**
1. **查看冲突文件**：
   ```powershell
   git status
   ```

2. **手动解决冲突**：
   - 打开冲突文件，找到冲突标记 `<<<<<<<`, `=======`, `>>>>>>>`
   - 编辑文件，保留需要的更改
   - 移除冲突标记

3. **完成合并**：
   ```powershell
   git add .
   git commit -m "fix: 解决合并冲突"
   git push origin develop
   ```

### 2.2 构建检查失败

**症状：**
- 提交前构建检查失败
- 前端构建错误或后端编译错误

**可能原因：**
- 代码语法错误
- 依赖版本不兼容
- 类型定义错误

**解决方案：**
1. **检查构建错误信息**：
   - 查看 npm run build 或 mvn compile 的错误输出

2. **修复错误**：
   - 修复代码语法错误
   - 更新依赖版本
   - 修复类型定义错误

3. **重新运行构建检查**：
   ```powershell
   # 前端
   cd oc-platform-web
   npm run build
   
   # 后端
   mvn clean compile
   ```

### 2.3 代码规范检查失败

**症状：**
- 提交前代码规范检查失败
- ESLint 错误或警告

**可能原因：**
- 代码不符合 ESLint 规则
- 代码格式不正确

**解决方案：**
1. **运行代码格式化**：
   ```powershell
   cd oc-platform-web
   npm run format
   ```

2. **修复 ESLint 错误**：
   ```powershell
   cd oc-platform-web
   npm run lint
   # 根据错误信息修复代码
   ```

3. **更新 ESLint 配置**：
   - 根据项目需求调整 ESLint 规则

### 2.4 分支管理问题

**症状：**
- 分支过多或混乱
- 无法找到正确的分支
- 分支合并错误

**可能原因：**
- 分支命名不规范
- 分支管理不当
- 合并策略错误

**解决方案：**
1. **清理过期分支**：
   ```powershell
   # 查看本地分支
   git branch
   
   # 删除已合并的分支
   git branch -d <branch>
   
   # 清理远程已删除的分支
   git fetch --prune
   ```

2. **规范分支命名**：
   - 功能分支：`feature/功能名称`
   - 发布分支：`release/版本号`
   - 热修复分支：`hotfix/修复描述`

3. **使用 GitFlow 工作流**：
   - 遵循 GitFlow 分支管理策略
   - 正确使用功能分支、发布分支和热修复分支

## 3. 通用 Git 问题

### 3.1 撤销提交

**症状：**
- 提交了错误的代码
- 需要撤销最近的提交

**解决方案：**
1. **撤销提交但保留更改**：
   ```powershell
   git reset --soft HEAD~1
   ```

2. **撤销提交且丢弃更改（谨慎使用）**：
   ```powershell
   git reset --hard HEAD~1
   ```

3. **撤销远程提交**：
   ```powershell
   git reset --soft HEAD~1
   git push origin <branch> --force-with-lease
   ```

### 3.2 查看提交历史

**症状：**
- 需要查看提交历史
- 查找特定的提交

**解决方案：**
1. **查看简洁历史**：
   ```powershell
   git log --oneline -10
   ```

2. **查看详细历史**：
   ```powershell
   git log --graph --oneline --all
   ```

3. **查看特定文件的历史**：
   ```powershell
   git log --oneline -p -- <file>
   ```

4. **查看特定作者的提交**：
   ```powershell
   git log --author="John Doe" --oneline
   ```

### 3.3 仓库维护

**症状：**
- 仓库体积过大
- Git 操作速度慢

**解决方案：**
1. **垃圾回收**：
   ```powershell
   git gc
   ```

2. **清理未引用的对象**：
   ```powershell
   git prune
   ```

3. **压缩历史**：
   ```powershell
   git repack -a -d --depth=250 --window=250
   ```

4. **定期备份**：
   ```powershell
   # 创建备份分支
   git checkout -b backup/$(Get-Date -Format "yyyy-MM-dd")
   git push origin backup/$(Get-Date -Format "yyyy-MM-dd")
   git checkout main
   ```

### 3.4 远程仓库配置

**症状：**
- 远程仓库配置错误
- 无法推送到正确的远程仓库

**解决方案：**
1. **查看远程仓库**：
   ```powershell
   git remote -v
   ```

2. **添加远程仓库**：
   ```powershell
   git remote add origin https://github.com/K-irito02/oc.git
   ```

3. **修改远程仓库 URL**：
   ```powershell
   git remote set-url origin https://github.com/K-irito02/oc.git
   ```

4. **删除远程仓库**：
   ```powershell
   git remote remove origin
   ```

## 4. 脚本使用问题

### 4.1 脚本执行权限

**症状：**
- 脚本无法执行
- 提示 "无法加载文件 ... 因为在此系统上禁止运行脚本"

**解决方案：**
1. **修改执行策略**：
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **直接执行脚本**：
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\commit-env.ps1 -Type config -Message "更新配置"
   ```

### 4.2 脚本参数错误

**症状：**
- 脚本执行失败
- 提示参数错误

**解决方案：**
1. **查看脚本帮助**：
   ```powershell
   Get-Help .\scripts\commit-env.ps1
   ```

2. **正确传递参数**：
   ```powershell
   # 环境状态仓库
   .\scripts\commit-env.ps1 -Type config -Message "更新AI技能"
   
   # 项目代码仓库
   .\scripts\quick-commit.ps1 -Type feat -Message "添加新功能" -Branch develop
   ```

3. **检查参数类型**：
   - 确保传递的参数类型正确
   - 对于字符串参数，确保使用引号包围

### 4.3 脚本路径问题

**症状：**
- 脚本无法找到文件
- 路径错误

**解决方案：**
1. **使用绝对路径**：
   ```powershell
   & "e:\oc\scripts\commit-env.ps1" -Type config -Message "更新配置"
   ```

2. **检查工作目录**：
   - 确保在正确的目录中执行脚本
   - 脚本会自动切换到正确的工作目录

## 5. 团队协作问题

### 5.1 代码审查流程

**症状：**
- 代码审查流程不顺畅
- PR 合并延迟

**解决方案：**
1. **规范 PR 描述**：
   - 清晰描述 PR 的目的和变更
   - 包含相关的 issue 链接
   - 提供测试说明

2. **设置审查规则**：
   - 要求至少一个审查者批准
   - 配置 CI/CD 检查
   - 要求通过所有测试

3. **及时响应审查**：
   - 及时回复审查评论
   - 快速修复审查中提出的问题
   - 保持 PR 小而专注

### 5.2 分支冲突

**症状：**
- 频繁出现分支冲突
- 合并困难

**解决方案：**
1. **定期合并 develop 分支**：
   ```powershell
   # 在功能分支中
   git checkout develop
   git pull origin develop
   git checkout feature/新功能
   git merge develop
   ```

2. **使用 rebase 保持线性历史**：
   ```powershell
   git checkout feature/新功能
   git rebase develop
   ```

3. **小批量提交**：
   - 避免一次提交过多更改
   - 保持提交专注于单一功能

### 5.3 版本控制混乱

**症状：**
- 版本号管理混乱
- 发布流程不清晰

**解决方案：**
1. **使用语义化版本**：
   - 遵循 Semantic Versioning 规范
   - 版本号格式：MAJOR.MINOR.PATCH

2. **规范发布流程**：
   - 使用发布分支进行测试
   - 合并到 main 分支后打标签
   - 发布后同步到 develop 分支

3. **自动化版本管理**：
   - 使用工具管理版本号
   - 配置 CI/CD 自动生成版本号

## 6. 性能优化问题

### 6.1 Git 操作速度慢

**症状：**
- Git 命令执行缓慢
- 推送和拉取操作耗时较长

**解决方案：**
1. **启用 Git 压缩**：
   ```powershell
   git config --global core.compression 9
   ```

2. **使用 shallow clone**：
   ```powershell
   git clone --depth 1 https://github.com/K-irito02/oc.git
   ```

3. **清理本地缓存**：
   ```powershell
   git gc --aggressive --prune=now
   ```

4. **使用 SSH 协议**：
   ```powershell
   git remote set-url origin git@github.com:K-irito02/oc.git
   ```

### 6.2 构建时间长

**症状：**
- 前端构建时间长
- 后端编译时间长

**解决方案：**
1. **使用缓存**：
   - 启用 npm 缓存
   - 配置 Maven 本地仓库

2. **优化构建配置**：
   - 前端：使用 Vite 或 Webpack 缓存
   - 后端：使用 Maven 增量构建

3. **并行构建**：
   - 前端：使用 `npm run build -- --parallel`
   - 后端：使用 `mvn compile -T 1C`

## 7. 安全问题

### 7.1 敏感信息泄露

**症状：**
- 提交中包含敏感信息
- GitHub 检测到密钥

**解决方案：**
1. **移除敏感信息**：
   - 使用 BFG Repo-Cleaner 从历史中移除敏感信息
   - 或使用 `git filter-branch`

2. **使用环境变量**：
   - 将敏感信息存储在环境变量中
   - 使用 `.env` 文件并添加到 `.gitignore`

3. **配置预提交钩子**：
   - 使用 `pre-commit` 钩子检查敏感信息
   - 配置 `detect-secrets` 工具

### 7.2 权限问题

**症状：**
- 无法推送或拉取代码
- 权限被拒绝

**解决方案：**
1. **检查仓库权限**：
   - 确保用户有正确的仓库权限
   - 检查组织权限设置

2. **配置 SSH 密钥**：
   - 生成 SSH 密钥
   - 添加到 GitHub 账户

3. **使用个人访问令牌**：
   - 生成具有适当权限的 PAT
   - 使用 PAT 进行认证

## 8. 常见问题解答

### Q: 如何撤销已经推送到远程仓库的提交？

**A:** 可以使用以下命令：
```powershell
# 撤销最近一次提交
git reset --soft HEAD~1

# 强制推送到远程仓库
git push origin <branch> --force-with-lease
```

**注意：** 这会修改远程仓库的历史，谨慎使用，尤其是在多人协作的分支上。

### Q: 如何处理 Git 合并冲突？

**A:** 处理 Git 合并冲突的步骤：
1. 查看冲突文件：`git status`
2. 打开冲突文件，找到冲突标记 `<<<<<<<`, `=======`, `>>>>>>>`
3. 编辑文件，保留需要的更改，移除冲突标记
4. 完成合并：`git add .` 和 `git commit -m "fix: 解决合并冲突"`

### Q: 如何清理本地和远程的过期分支？

**A:** 清理分支的步骤：
1. 清理本地已合并的分支：`git branch -d <branch>`
2. 清理远程已删除的分支：`git fetch --prune`
3. 查看所有分支：`git branch -a`

### Q: 如何优化 Git 仓库大小？

**A:** 优化 Git 仓库大小的方法：
1. 运行垃圾回收：`git gc`
2. 压缩历史：`git repack -a -d --depth=250 --window=250`
3. 移除大文件：使用 `git filter-branch` 或 BFG Repo-Cleaner
4. 使用 shallow clone：`git clone --depth 1 <url>`

### Q: 如何设置 Git 提交模板？

**A:** 设置 Git 提交模板的步骤：
1. 创建提交模板文件 `.gitmessage`
2. 配置 Git 使用模板：`git config --global commit.template .gitmessage`
3. 模板内容示例：
   ```
   <type>: <description>
   
   <body>
   
   <footer>
   ```

### Q: 如何使用 Git 子模块？

**A:** 使用 Git 子模块的步骤：
1. 添加子模块：`git submodule add <url> <path>`
2. 初始化子模块：`git submodule init`
3. 更新子模块：`git submodule update --remote`
4. 克隆包含子模块的仓库：`git clone --recursive <url>`

## 9. 总结

Git 提交工作流是项目开发中重要的一部分，正确使用和管理 Git 可以提高开发效率和代码质量。通过本故障排除指南，您应该能够解决常见的 Git 问题，并优化您的 Git 工作流。

**关键要点：**
- 遵循 GitFlow 分支管理策略
- 使用规范的提交信息格式
- 定期进行代码审查和构建检查
- 合理管理分支和标签
- 保护敏感信息，避免泄露
- 定期维护和优化 Git 仓库

如果您遇到本指南未覆盖的问题，请参考 Git 官方文档或寻求社区支持。