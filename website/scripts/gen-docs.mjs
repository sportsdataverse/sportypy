// Runs tools/gen_docs.py before `yarn start` and `yarn build` (the prestart and
// prebuild scripts), so the reference is rebuilt from the docstrings on every
// build: locally, in CI and on Vercel. It needs uv; where uv is missing (the
// Vercel build image) it installs it with pip first.
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const run = (cmd, args) => spawnSync(cmd, args, {cwd: repo, stdio: 'inherit', shell: process.platform === 'win32'});
const has = (cmd, args) => spawnSync(cmd, args, {stdio: 'ignore', shell: process.platform === 'win32'}).status === 0;

let uv = ['uv'];
if (!has('uv', ['--version'])) {
  const python = has('python3', ['--version']) ? 'python3' : 'python';
  console.log('gen-docs: uv not found, installing it with pip');
  if (run(python, ['-m', 'pip', 'install', '--quiet', '--user', 'uv']).status !== 0) {
    run(python, ['-m', 'pip', 'install', '--quiet', '--break-system-packages', 'uv']);
  }
  uv = [python, '-m', 'uv'];
}

const [cmd, ...pre] = uv;
const result = run(cmd, [...pre, 'run', '--frozen', '--no-default-groups', '--group', 'docs', 'python', 'tools/gen_docs.py']);
process.exit(result.status ?? 1);
