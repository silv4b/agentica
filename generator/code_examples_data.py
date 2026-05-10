CODE_EXAMPLES = {}

# ── Batch 1: JavaScript / TypeScript ──────────────────────────

CODE_EXAMPLES["angular"] = {
    "examples": """## Code Examples

Good:
```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly http = inject(HttpClient);

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users').pipe(
      catchError(this.handleError)
    );
  }
}
```

Bad:
```typescript
export class UserService {
  constructor(private http: HttpClient) {}

  getUsers(): Observable<any> {
    return this.http.get('/api/users');
  }
}
```""",
    "boundaries": """## Boundaries

- Always: Use standalone components, signals, typed reactive forms, OnPush change detection
- Ask first: Custom NgModules, direct DOM manipulation, custom change detection strategies
- Never: Use `any` type, disable `strictTemplates`, mix template-driven and reactive forms\n""",
}

CODE_EXAMPLES["express"] = {
    "examples": """## Code Examples

Good:
```typescript
import { Router } from 'express';

const router = Router();

router.get('/users', async (req, res, next) => {
  try {
    const users = await userService.findAll();
    res.json({ data: users });
  } catch (err) {
    next(err);
  }
});
```

Bad:
```javascript
app.get('/users', function(req, res) {
  db.query('SELECT * FROM users', (err, rows) => {
    res.send(rows);
  });
});
```""",
    "boundaries": """## Boundaries

- Always: Use async/await, centralized error handling middleware, helmet + cors
- Ask first: Synchronous route handlers, custom session middleware, raw SQL queries
- Never: Use `next(err)` without error handler, expose stack traces in production, disable CORS entirely""",
}

CODE_EXAMPLES["jest"] = {
    "examples": """## Code Examples

Good:
```typescript
describe('UserService', () => {
  it('returns users when API succeeds', async () => {
    const users = await userService.findAll();
    expect(users).toHaveLength(3);
    expect(users[0]).toMatchObject({ id: expect.any(Number) });
  });
});
```

Bad:
```javascript
test('user service', () => {
  return userService.findAll().then(users => {
    expect(users.length).toBe(3);
  });
});
```""",
    "boundaries": """## Boundaries

- Always: Use `describe`/`it` blocks, `toEqual`/`toMatchObject`, mock external services
- Ask first: Snapshot tests for large objects, custom matchers, manual mocks
- Never: Use `.only` in committed code, mock what you don't own, test implementation details""",
}

CODE_EXAMPLES["jquery"] = {
    "examples": """## Code Examples

Good:
```javascript
const $list = $('#user-list');

$list.on('click', '.user-item', function() {
  const id = $(this).data('id');
  loadUserDetail(id);
});
```

Bad:
```javascript
$('.user-item').click(function() {
  var id = $(this).attr('data-id');
  $.get('/user/' + id, function(data) {
    $('#user-detail').html(data);
  });
});
```""",
    "boundaries": """## Boundaries

- Always: Use event delegation with `.on()`, cache selectors, chain methods
- Ask first: New jQuery usage on greenfield projects (prefer vanilla JS or framework)
- Never: Use deprecated `.click()`, `.bind()`, `.live()`, mix jQuery with framework DOM manipulation""",
}

CODE_EXAMPLES["nestjs"] = {
    "examples": """## Code Examples

Good:
```typescript
@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  async findAll(): Promise<User[]> {
    return this.userService.findAll();
  }
}
```

Bad:
```typescript
@Controller()
export class Users {
  @Get('/users')
  getUsers(req, res) {
    res.json({ data: [] });
  }
}
```""",
    "boundaries": """## Boundaries

- Always: Use modules for feature organization, DTOs for validation, dependency injection
- Ask first: Custom providers, dynamic modules, circular dependencies
- Never: Use raw `req`/`res` in controllers, skip validation pipes, mix responsibilities in modules""",
}

CODE_EXAMPLES["next.js"] = {
    "examples": """## Code Examples

Good:
```typescript
// app/users/page.tsx
export default async function UsersPage() {
  const users = await fetchUsers();
  return <UserList users={users} />;
}
```

Bad:
```typescript
// pages/users.jsx
export default function UsersPage() {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers);
  }, []);
  return <div>{users.map(u => <p>{u.name}</p>)}</div>;
}
```""",
    "boundaries": """## Boundaries

- Always: Use App Router, Server Components by default, `next/image` for images
- Ask first: Pages Router, client-side data fetching, custom server
- Never: Use `useEffect` for data fetching (prefer server components), disable SSR without reason""",
}

CODE_EXAMPLES["node"] = {
    "examples": """## Code Examples

Good:
```typescript
import { readFile } from 'fs/promises';

export async function loadConfig(path: string): Promise<Config> {
  const content = await readFile(path, 'utf-8');
  return JSON.parse(content);
}
```

Bad:
```javascript
const fs = require('fs');

function loadConfig(path) {
  const data = fs.readFileSync(path, 'utf-8');
  return JSON.parse(data);
}
```""",
    "boundaries": """## Boundaries

- Always: Use ES modules (`import`/`export`), `fs/promises`, environment variables for config
- Ask first: `require`, synchronous I/O in request handlers, process global state
- Never: Ignore unhandled promise rejections, use `process.exit()` manually, store secrets in code""",
}

CODE_EXAMPLES["nuxt.js"] = {
    "examples": """## Code Examples

Good:
```typescript
// composables/useUsers.ts
export const useUsers = () => {
  return useAsyncData('users', () => $fetch('/api/users'));
};
```

Bad:
```vue
<script setup>
const users = ref([]);
onMounted(async () => {
  const res = await fetch('/api/users');
  users.value = await res.json();
});
</script>
```""",
    "boundaries": """## Boundaries

- Always: Use Nuxt 3, auto-imports, `useAsyncData`/`useFetch`, `definePageMeta`
- Ask first: Custom plugins, manual Vuex, `@nuxtjs/axios` (use `$fetch` instead)
- Never: Use Nuxt 2 patterns, manually import composables, use `fetch` hook""",
}

CODE_EXAMPLES["playwright"] = {
    "examples": """## Code Examples

Good:
```typescript
test('user can log in', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name=email]', 'user@example.com');
  await page.fill('[name=password]', 'secret');
  await page.click('button[type=submit]');
  await expect(page.locator('.welcome')).toBeVisible();
});
```

Bad:
```javascript
test('login', async ({ page }) => {
  await page.goto('/login');
  await page.type('#email', 'user@example.com');
  await page.type('#password', 'secret');
  await page.click('button');
  await page.waitForTimeout(2000);
  expect(await page.textContent('.welcome')).toBe('Hello');
});
```""",
    "boundaries": """## Boundaries

- Always: Use Page Object Model, `locator` over `$()`, `toBeVisible`/`toHaveText` assertions
- Ask first: `waitForTimeout`, `page.evaluate`, browser contexts per test
- Never: Use `waitForTimeout` for timing, rely on `sleep`, share page state between tests""",
}

CODE_EXAMPLES["react"] = {
    "examples": """## Code Examples

Good:
```typescript
function UserList() {
  const { data: users, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  if (isLoading) return <Skeleton />;
  return <ul>{users?.map(user => <UserItem key={user.id} user={user} />)}</ul>;
}
```

Bad:
```javascript
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(data => {
      setUsers(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading...</div>;
  return <ul>{users.map(user => <li key={user.id}>{user.name}</li>)}</ul>;
}
```""",
    "boundaries": """## Boundaries

- Always: Use functional components + hooks, TypeScript, React Query or SWR for server state
- Ask first: Class components, `useReducer` over `useState`, custom refs for DOM access
- Never: Use `useEffect` for data fetching (use a library), mutate state directly, index as `key`""",
}

CODE_EXAMPLES["svelte"] = {
    "examples": """## Code Examples

Good:
```svelte
<script lang="ts">
  let { user }: { user: User } = $props();
  let fullName = $derived(`${user.firstName} ${user.lastName}`);
</script>

<h1>{fullName}</h1>
```

Bad:
```svelte
<script>
  export let user;
  let fullName = '';
  $: fullName = user.firstName + ' ' + user.lastName;
</script>

<h1>{fullName}</h1>
```""",
    "boundaries": """## Boundaries

- Always: Use Svelte 5 runes (`$state`, `$derived`, `$props`), SvelteKit for full-stack apps
- Ask first: Svelte 4 reactivity (`$:` syntax), manual stores, custom transitions
- Never: Use `on:click` without proper typing, mutate `$state` outside reactive context""",
}

CODE_EXAMPLES["typescript"] = {
    "examples": """## Code Examples

Good:
```typescript
interface User {
  readonly id: number;
  name: string;
  email?: string;
}

type ApiResponse<T> = {
  data: T;
  error: null | string;
};
```

Bad:
```typescript
interface User {
  id: number;
  name: string;
  email: string | undefined;
}

type ApiResponse = {
  data: any;
  error: string | null;
};
```""",
    "boundaries": """## Boundaries

- Always: Enable `strict: true`, prefer `interface` over `type` for objects, use `unknown` over `any`
- Ask first: `namespace`, `@ts-ignore`, `as any` casts
- Never: Disable `strict`, use `any` without explicit reason, use `ts-ignore` as default""",
}

CODE_EXAMPLES["vite"] = {
    "examples": """## Code Examples

Good:
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: { target: 'es2020' },
});
```

Bad:
```javascript
// vite.config.js
module.exports = {
  plugins: ['react'],
};
```""",
    "boundaries": """## Boundaries

- Always: Use TypeScript config, official Vite plugins, environment variables with `import.meta.env`
- Ask first: Custom rollup plugins, manual chunk splitting, non-standard asset handling
- Never: Disable HMR, use Webpack-style config, mix build tools""",
}

CODE_EXAMPLES["vitest"] = {
    "examples": """## Code Examples

Good:
```typescript
import { describe, it, expect, vi } from 'vitest';

vi.mock('../services/user');

describe('UserList', () => {
  it('renders users', async () => {
    const { container } = render(<UserList />);
    expect(container).toHaveTextContent('John');
  });
});
```

Bad:
```javascript
test('user list', () => {
  const { container } = render(UserList);
  expect(container.innerHTML).toContain('John');
});
```""",
    "boundaries": """## Boundaries

- Always: Share Vite config between app and tests, use `vi.mock()` / `vi.spyOn()`, `@vitest/coverage-v8`
- Ask first: Jest-compatible mocks, custom environments, snapshot testing
- Never: Use Jest-specific APIs (use Vitest equivalents), mock modules without `vi.mock`""",
}

CODE_EXAMPLES["vue"] = {
    "examples": """## Code Examples

Good:
```vue
<script setup lang="ts">
interface Props { user: User }
const props = defineProps<Props>();
const emit = defineEmits<{ update: [id: number] }>();
</script>

<template>
  <button @click="emit('update', user.id)">{{ user.name }}</button>
</template>
```

Bad:
```vue
<script>
export default {
  props: ['user'],
  methods: {
    update() { this.$emit('update', this.user.id); }
  }
};
</script>

<template>
  <button @click="update">{{ user.name }}</button>
</template>
```""",
    "boundaries": """## Boundaries

- Always: Use Composition API with `<script setup>`, TypeScript, Pinia for state management
- Ask first: Options API, Vuex, `this.$refs` for DOM access
- Never: Use index as `:key` in `v-for`, mutate props directly, use `$parent` for communication""",
}

# ── Batch 2: Python ────────────────────────────────────────────

CODE_EXAMPLES["fastapi"] = {
    "examples": """## Code Examples

Good:
```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class UserResponse(BaseModel):
    id: int
    name: str

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db=Depends(get_db)):
    user = await db.fetch_user(user_id)
    return user
```

Bad:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id):
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    return {"id": user.id, "name": user.name}
```""",
    "boundaries": """## Boundaries

- Always: Use Pydantic models for request/response, dependency injection, async endpoints
- Ask first: Synchronous endpoints for CPU-bound work, custom middleware, sub-applications
- Never: Return raw dicts without validation, suppress type errors, use `response_model=None`""",
}

CODE_EXAMPLES["flask"] = {
    "examples": """## Code Examples

Good:
```python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/users/<int:user_id>")
def get_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return jsonify(id=user.id, name=user.name)
```

Bad:
```python
from flask import Flask

app = Flask(__name__)

@app.route("/users/<user_id>")
def get_user(user_id):
    user = db.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return {"id": user.id}
```""",
    "boundaries": """## Boundaries

- Always: Use blueprints for modularity, application factory pattern, type hints
- Ask first: Flask-RESTful, custom decorators for routes, global state
- Never: Use string formatting in SQL queries, put business logic in routes, disable CSRF in production""",
}

CODE_EXAMPLES["uv"] = {
    "examples": """## Code Examples

Good:
```bash
uv init my-project
cd my-project
uv add fastapi uvicorn
uv add --dev pytest
uv run uvicorn main:app
```

Bad:
```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install fastapi uvicorn pytest
python main.py
```""",
    "boundaries": """## Boundaries

- Always: Use `uv.lock` for reproducibility, `uv add --dev` for dev deps, `pyproject.toml` as source of truth
- Ask first: Mixing pip and uv, editable installs, platform-specific dependencies
- Never: Commit `uv.lock` without `pyproject.toml`, use `pip` alongside uv without reason""",
}

# ── Batch 3: C# / .NET ─────────────────────────────────────────

CODE_EXAMPLES["aspnetcore"] = {
    "examples": """## Code Examples

Good:
```csharp
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;

    public UsersController(IUserService userService)
    {
        _userService = userService;
    }

    [HttpGet]
    public async Task<ActionResult<List<User>>> GetAll()
    {
        var users = await _userService.GetAllAsync();
        return Ok(users);
    }
}
```

Bad:
```csharp
public class UsersController : Controller
{
    private readonly AppDbContext _db;

    public UsersController()
    {
        _db = new AppDbContext();
    }

    public IActionResult Index()
    {
        return View(_db.Users.ToList());
    }
}
```""",
    "boundaries": """## Boundaries

- Always: Use dependency injection, async/await, file-scoped namespaces, records for DTOs
- Ask first: Custom middleware, synchronous I/O, raw ADO.NET
- Never: Use `new` for services, ignore cancellation tokens, expose full domain models as API responses""",
}

CODE_EXAMPLES["blazor"] = {
    "examples": """## Code Examples

Good:
```razor
@page "/users"
@inject IUserService UserService

@if (users is null)
{
    <Loading />
}
else
{
    @foreach (var user in users)
    {
        <UserCard User="@user" />
    }
}

@code {
    private List<User>? users;

    protected override async Task OnInitializedAsync()
    {
        users = await UserService.GetAllAsync();
    }
}
```

Bad:
```razor
@page "/users"
@inject HttpClient Http

@foreach (var user in await Http.GetFromJsonAsync<User[]>("/api/users"))
{
    <div>@user.Name</div>
}
```""",
    "boundaries": """## Boundaries

- Always: Use CSS isolation, dependency injection, `@rendermode` for interactivity, proper loading states
- Ask first: JavaScript interop for complex DOM, manual state management, render mode per component
- Never: Mix server and WebAssembly without clear separation, ignore disposal of resources""",
}

CODE_EXAMPLES["csharp"] = {
    "examples": """## Code Examples

Good:
```csharp
public record UserDto(int Id, string Name, string? Email);

public interface IUserRepository
{
    Task<UserDto?> GetByIdAsync(int id);
}

public class UserService(IUserRepository repo) : IUserService
{
    public async Task<UserDto?> GetUserAsync(int id) => await repo.GetByIdAsync(id);
}
```

Bad:
```csharp
public class User
{
    public int Id;
    public string Name;
    public string Email;
}

public class UserService
{
    public User GetUser(int id)
    {
        return db.Users.Find(id);
    }
}
```""",
    "boundaries": """## Boundaries

- Always: Use `var` when type is obvious, expression-bodied members, `record` for immutable data
- Ask first: Dynamic types, reflection-heavy patterns, `Newtonsoft.Json` (prefer `System.Text.Json`)
- Never: Ignore nullable reference types, use `throw new Exception()` (use specific exceptions)""",
}

# ── Batch 4: Java / Kotlin ─────────────────────────────────────

CODE_EXAMPLES["java"] = {
    "examples": """## Code Examples

Good:
```java
@Service
public class UserService {
    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }

    public Optional<User> findById(long id) {
        return repository.findById(id);
    }
}
```

Bad:
```java
public class UserService {
    private UserRepository repository = new UserRepository();

    public User findById(long id) {
        return repository.findById(id).orElse(null);
    }
}
```""",
    "boundaries": """## Boundaries

- Always: Use Optional over null returns, try-with-resources, SLF4J for logging, JUnit 5
- Ask first: Custom class loaders, reflection, checked exceptions in lambdas
- Never: Use raw types, suppress warnings without justification, return null from Optional-returning methods""",
}

CODE_EXAMPLES["kotlin"] = {
    "examples": """## Code Examples

Good:
```kotlin
data class User(val id: Long, val name: String, val email: String?)

@Service
class UserService(private val repo: UserRepository) {
    suspend fun getUser(id: Long): User? = repo.findById(id)
}
```

Bad:
```kotlin
class User(val id: Long, val name: String, val email: String?)

class UserService(val repo: UserRepository) {
    fun getUser(id: Long): User? {
        return repo.findById(id)
    }
}
```""",
    "boundaries": """## Boundaries

- Always: Use `val` over `var`, nullable types explicitly with `?`, data classes for models, coroutines for async
- Ask first: Java interop for complex APIs, `object` declarations for singletons, companion objects
- Never: Use `!!` without justification, ignore coroutine cancellation, use `var` for immutable references""",
}

CODE_EXAMPLES["spring"] = {
    "examples": """## Code Examples

Good:
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService service;

    @GetMapping
    public ResponseEntity<List<User>> getAll() {
        return ResponseEntity.ok(service.findAll());
    }
}
```

Bad:
```java
@RestController
public class UserController {
    @Autowired
    private UserService service;

    @GetMapping("/api/users")
    public List<User> getAll() {
        return service.findAll();
    }
}
```""",
    "boundaries": """## Boundaries

- Always: Use constructor injection over `@Autowired`, `ResponseEntity` for responses, validation annotations
- Ask first: Field injection, `@Transactional` on controller methods, raw `@Query` without validation
- Never: Use `@Autowired` on fields, catch `Exception` broadly, expose internal entities as API responses""",
}

CODE_EXAMPLES["springboot"] = {
    "examples": """## Code Examples

Good:
```yaml
# application.yml
spring:
  datasource:
    url: ${DATABASE_URL}
    hikari.maximum-pool-size: 10
```

Bad:
```properties
# application.properties
spring.datasource.url=jdbc:postgresql://localhost:5432/db
spring.datasource.password=secret123
```""",
    "boundaries": """## Boundaries

- Always: Use YAML over properties, externalize config via `${VARIABLE}`, use `@ConfigurationProperties`
- Ask first: Auto-configuration exclusions, custom `@Conditional`, multiple datasources
- Never: Hardcode secrets in config files, disable actuator endpoints in production, use `@SpringBootApplication` scan without `basePackages`""",
}

# ── Batch 5: SQL / Database ────────────────────────────────────

CODE_EXAMPLES["sqlite"] = {
    "examples": """## Code Examples

Good:
```sql
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

BEGIN;
  INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
  INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');
COMMIT;
```

Bad:
```sql
CREATE TABLE users (
    id   INTEGER,
    name TEXT,
    email TEXT
);

INSERT INTO users VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO users VALUES (2, 'Bob', 'bob@example.com');
```""",
    "boundaries": """## Boundaries

- Always: Enable WAL mode, enable foreign keys (`PRAGMA foreign_keys = ON`), use `BEGIN`/`COMMIT` for batch operations
- Ask first: `VACUUM` frequently, custom collation, `ATTACH DATABASE`
- Never: Use `INTEGER PRIMARY KEY` without `AUTOINCREMENT` (if order matters), disable fsync, use without proper indexing""",
}

CODE_EXAMPLES["postgresql"] = {
    "examples": """## Code Examples

Good:
```sql
CREATE TABLE users (
    id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name  VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE INDEX idx_users_email ON users (email);

SELECT * FROM users WHERE email = $1;
```

Bad:
```sql
CREATE TABLE users (
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL
);

SELECT * FROM users WHERE email = '" + userInput + "';
```""",
    "boundaries": """## Boundaries

- Always: Use UUIDs for primary keys, parameterized queries, appropriate indexes, `EXPLAIN ANALYZE` for optimization
- Ask first: Raw string concatenation, `NOT IN` on subqueries, unlogged tables
- Never: Use string interpolation in queries, disable `ssl` in production, use `SELECT *` in production code""",
}

CODE_EXAMPLES["mysql"] = {
    "examples": """## Code Examples

Good:
```sql
CREATE TABLE users (
    id    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Bad:
```sql
CREATE TABLE users (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL
);
```""",
    "boundaries": """## Boundaries

- Always: Use InnoDB engine, `utf8mb4` charset, proper indexes, `EXPLAIN` for query analysis
- Ask first: MyISAM, `ENUM` types, `SELECT ... FOR UPDATE`
- Never: Use `utf8` (alias for utf8mb3), omit `WHERE` in `UPDATE`/`DELETE`, use string interpolation in queries""",
}

CODE_EXAMPLES["mariadb"] = {
    "examples": """## Code Examples

Good:
```sql
CREATE TABLE users (
    id    INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Bad:
```sql
CREATE TABLE users (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL
) ENGINE=MyISAM;
```""",
    "boundaries": """## Boundaries

- Always: Use InnoDB (or Aria), `utf8mb4` charset, sequence engines over `AUTO_INCREMENT` for complex needs
- Ask first: Cassandra/Storage Engine-specific features, CONNECT engine
- Never: Use `utf8` (alias for utf8mb3), skip `EXPLAIN` on slow queries, use string concatenation in queries""",
}

CODE_EXAMPLES["mongodb"] = {
    "examples": """## Code Examples

Good:
```javascript
db.users.createIndex({ email: 1 }, { unique: true });

db.users.insertOne({
  name: "Alice",
  email: "alice@example.com",
  roles: ["admin"]
});
```

Bad:
```javascript
db.users.insertOne({
  name: "Alice",
  email: "alice@example.com",
  roles: "admin"
});
```""",
    "boundaries": """## Boundaries

- Always: Create indexes for query patterns, use schema validation, use aggregation pipeline over client-side joins
- Ask first: Embedded documents for frequently-changing data, `$where` operator, multi-document transactions
- Never: Use without indexing, embed unbounded arrays, disable journaling in production""",
}

CODE_EXAMPLES["redis"] = {
    "examples": """## Code Examples

Good:
```python
import redis.asyncio as redis

r = redis.Redis(connection_pool=redis.ConnectionPool(decode_responses=True))
await r.setex("session:123", 3600, user_data)
session = await r.get("session:123")
```

Bad:
```python
import redis

r = redis.Redis()
r.set("session:123", user_data)
r.expire("session:123", 3600)
```""",
    "boundaries": """## Boundaries

- Always: Use connection pooling, set TTL on all keys, use appropriate data types (hashes, sets, sorted sets)
- Ask first: `KEYS` in production, transactions (`MULTI`/`EXEC`), Lua scripting
- Never: Use as primary database, store large blobs, use `KEYS *` in production, disable persistence without reason""",
}

# ── Batch 6: Go / Rust ─────────────────────────────────────────

CODE_EXAMPLES["go"] = {
    "examples": """## Code Examples

Good:
```go
package user

type Service struct {
    repo Repository
}

func (s *Service) GetUser(ctx context.Context, id int64) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("get user %d: %w", id, err)
    }
    return user, nil
}
```

Bad:
```go
func getUser(id int64) *User {
    row := db.QueryRow("SELECT * FROM users WHERE id = ?", id)
    user := &User{}
    row.Scan(&user.ID, &user.Name)
    return user
}
```""",
    "boundaries": """## Boundaries

- Always: Handle errors explicitly, use `context.Context` for cancellation, write table-driven tests
- Ask first: Panic for control flow, `init()` functions that can fail, global state
- Never: Ignore errors with `_`, use `panic` for routine errors, use `interface{}` over generics (Go 1.18+)""",
}

CODE_EXAMPLES["rust"] = {
    "examples": """## Code Examples

Good:
```rust
#[derive(Debug)]
pub struct User {
    pub id: i64,
    pub name: String,
}

pub fn find_user(id: i64) -> Result<User, AppError> {
    let user = repository::find(id).ok_or(AppError::NotFound)?;
    Ok(user)
}
```

Bad:
```rust
pub struct User {
    pub id: i64,
    pub name: String,
}

pub fn find_user(id: i64) -> User {
    match repository::find(id) {
        Some(user) => user,
        None => panic!("User not found"),
    }
}
```""",
    "boundaries": """## Boundaries

- Always: Use the type system to enforce invariants, `Result` over panics, `clippy` for linting
- Ask first: `unsafe` blocks, raw pointer manipulation, custom allocators
- Never: Use `unwrap()` without explanation, `panic!` for recoverable errors, ignore clippy warnings""",
}

# ── Batch 7: Ruby / PHP ────────────────────────────────────────

CODE_EXAMPLES["rails"] = {
    "examples": """## Code Examples

Good:
```ruby
# app/models/user.rb
class User < ApplicationRecord
  validates :email, presence: true, uniqueness: true
  has_many :posts, dependent: :destroy
end

# app/controllers/users_controller.rb
class UsersController < ApplicationController
  def index
    @users = User.all.page(params[:page])
  end
end
```

Bad:
```ruby
# No model validation
class UsersController < ApplicationController
  def index
    @users = User.all
  end
end
```""",
    "boundaries": """## Boundaries

- Always: Follow convention over configuration, use `ActiveRecord` validations, write tests with RSpec
- Ask first: Raw SQL, `find_each` vs `all.each` for large datasets, custom form objects
- Never: Skip database migrations, use `default_scope` without caution, put business logic in views""",
}

CODE_EXAMPLES["ruby"] = {
    "examples": """## Code Examples

Good:
```ruby
class UserService
  def initialize(repository: UserRepository.new)
    @repository = repository
  end

  def find(id)
    @repository.find(id) || raise(NotFoundError)
  end
end
```

Bad:
```ruby
class UserService
  def find(id)
    User.find(id)
  rescue ActiveRecord::RecordNotFound
    nil
  end
end
```""",
    "boundaries": """## Boundaries

- Always: Use Ruby 3.x pattern matching, keyword arguments, `freeze` for constants, write tests with Minitest/RSpec
- Ask first: `method_missing` for metaprogramming, `eval`/`class_eval`, global state
- Never: Use `unless` with complex conditions, modify core classes without reason, skip type checking (RBS/Sorbet)""",
}

CODE_EXAMPLES["laravel"] = {
    "examples": """## Code Examples

Good:
```php
class UserController extends Controller
{
    public function index(): JsonResponse
    {
        $users = User::with('posts')->paginate(15);
        return response()->json($users);
    }
}
```

Bad:
```php
class UserController extends Controller
{
    public function index()
    {
        $users = DB::select('SELECT * FROM users');
        return response()->json($users);
    }
}
```""",
    "boundaries": """## Boundaries

- Always: Use Eloquent ORM, migrations for schema changes, `with()` for eager loading, form requests for validation
- Ask first: Raw `DB::select`/`DB::statement`, `Query Builder` for complex queries, custom facades
- Never: Disable mass assignment protection, use `dd()`/`var_dump()` in committed code, skip pagination on large datasets""",
}

CODE_EXAMPLES["php"] = {
    "examples": """## Code Examples

Good:
```php
declare(strict_types=1);

class UserService
{
    public function __construct(
        private readonly UserRepository $repo
    ) {}

    public function find(int $id): ?User
    {
        return $this->repo->findById($id);
    }
}
```

Bad:
```php
class UserService
{
    public function find($id)
    {
        return db::query("SELECT * FROM users WHERE id = " . $id);
    }
}
```""",
    "boundaries": """## Boundaries

- Always: Use `declare(strict_types=1)`, typed properties, constructor promotion (PHP 8+), PSR-12
- Ask first: Global functions, `extract()`, `eval()`, dynamic properties
- Never: Use string interpolation in SQL queries, ignore return type declarations, use `mysql_*` functions""",
}

# ── Batch 8: CSS / Style ───────────────────────────────────────

CODE_EXAMPLES["css"] = {
    "examples": """## Code Examples

Good:
```css
:root {
  --color-primary: oklch(0.5 0.2 240);
  --spacing-unit: 0.5rem;
}

.card {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-unit);
  padding: calc(var(--spacing-unit) * 2);
}
```

Bad:
```css
.card {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  float: left;
  margin: 10px;
  padding: 10px;
}
```""",
    "boundaries": """## Boundaries

- Always: Use CSS custom properties for theme values, grid/flexbox over floats, `rem` for font sizes, mobile-first media queries
- Ask first: `!important` overrides, `@import` in CSS, absolute positioning for layout
- Never: Use `!important` as default, inline styles in production, `float` for layout""",
}

CODE_EXAMPLES["html"] = {
    "examples": """## Code Examples

Good:
```html
<header>
  <nav aria-label="Main">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>
<main>
  <h1>Welcome</h1>
  <img src="photo.jpg" alt="User photo" loading="lazy">
</main>
```

Bad:
```html
<div class="header">
  <div class="nav">
    <a href="/">Home</a>
    <a href="/about">About</a>
  </div>
</div>
<div>
  <h1>Welcome</h1>
  <img src="photo.jpg">
</div>
```""",
    "boundaries": """## Boundaries

- Always: Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`), proper heading hierarchy, `alt` on images
- Ask first: `<iframe>`, `<table>` for layout, `contenteditable` in production
- Never: Skip `alt` attributes, use `<div>` for everything, omit `lang` attribute on `<html>`""",
}

CODE_EXAMPLES["sass"] = {
    "examples": """## Code Examples

Good:
```scss
$color-primary: #2563eb;
$spacing-unit: 0.5rem;

@mixin respond-to($breakpoint) {
  @media (min-width: $breakpoint) { @content; }
}

.card {
  display: grid;
  gap: $spacing-unit;

  @include respond-to(768px) {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

Bad:
```scss
$primary: blue;
$space: 10px;

.card {
  display: grid;
  gap: 10px;
}

@media (min-width: 768px) {
  .card { grid-template-columns: repeat(2, 1fr); }
}
```""",
    "boundaries": """## Boundaries

- Always: Use variables/mixins for reuse, partials with `_` prefix, `@use` over `@import`
- Ask first: `@extend` for complex inheritance, nesting beyond 3 levels, global `@import`
- Never: Use `@import` (deprecated), create circular dependencies, deep nesting (>4 levels)""",
}

CODE_EXAMPLES["scss"] = CODE_EXAMPLES["sass"]

CODE_EXAMPLES["tailwind"] = {
    "examples": """## Code Examples

Good:
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
  <div class="rounded-lg shadow-md bg-white p-4 hover:shadow-lg transition-shadow">
    <h3 class="text-lg font-semibold text-gray-900">Card Title</h3>
    <p class="text-sm text-gray-600 mt-2">Card content here.</p>
  </div>
</div>
```

Bad:
```html
<div style="display: grid; grid-template-columns: 1fr; gap: 1rem; padding: 1.5rem;">
  <div style="border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h3 style="font-size: 1.125rem; font-weight: 600;">Card Title</h3>
  </div>
</div>
```""",
    "boundaries": """## Boundaries

- Always: Use utility classes directly in HTML, responsive prefixes (`sm:`, `md:`, `lg:`), `tailwind.config.js` for theme
- Ask first: `@apply` (prefer component classes), custom plugins, `!important` utilities
- Never: Mix Tailwind with inline styles, override Tailwind's reset, use `@apply` for utility-only components""",
}

CODE_EXAMPLES["daisyui"] = {
    "examples": """## Code Examples

Good:
```html
<div class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">User Profile</h2>
    <p>Welcome back, {{ user.name }}</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Edit</button>
    </div>
  </div>
</div>
```

Bad:
```html
<div class="card" style="background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
  <div>
    <h2>User Profile</h2>
    <p>Welcome back</p>
    <button style="background: blue; color: white;">Edit</button>
  </div>
</div>
```""",
    "boundaries": """## Boundaries

- Always: Use DaisyUI semantic classes (`btn`, `card`, `input`, `navbar`), customize theme in Tailwind config
- Ask first: Custom DaisyUI component variants, `data-theme` for multi-theme, `daisyui.config`
- Never: Use raw HTML elements over DaisyUI components, mix DaisyUI with custom CSS for same purpose""",
}

# ── Batch 9: Mobile ────────────────────────────────────────────

CODE_EXAMPLES["dart"] = {
    "examples": """## Code Examples

Good:
```dart
class User {
  final int id;
  final String name;
  final String? email;

  const User({required this.id, required this.name, this.email});
}

Future<User?> fetchUser(int id) async {
  final response = await http.get(Uri.parse('/api/users/$id'));
  if (response.statusCode == 200) {
    return User.fromJson(jsonDecode(response.body));
  }
  return null;
}
```

Bad:
```dart
class User {
  int id;
  String name;
  String email;
}

Future<dynamic> fetchUser(id) async {
  var response = await http.get(Uri.parse('/api/users/$id'));
  return jsonDecode(response.body);
}
```""",
    "boundaries": """## Boundaries

- Always: Use `const` constructors where possible, `final` over `var`, nullable types properly, pattern matching (Dart 3)
- Ask first: `dynamic` type, `late` without initialization, `!` null assertion
- Never: Use `var` for everything, ignore null safety, use `dynamic` over generics""",
}

CODE_EXAMPLES["flutter"] = {
    "examples": """## Code Examples

Good:
```dart
class UserCard extends StatelessWidget {
  const UserCard({super.key, required this.user});

  final User user;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(child: Text(user.initials)),
        title: Text(user.name),
        subtitle: Text(user.email ?? ''),
      ),
    );
  }
}
```

Bad:
```dart
class UserCard extends StatefulWidget {
  UserCard(this.user);
  final User user;

  @override
  State<UserCard> createState() => _UserCardState();
}

class _UserCardState extends State<UserCard> {
  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(widget.user.name),
      ),
    );
  }
}
```""",
    "boundaries": """## Boundaries

- Always: Use `StatelessWidget` by default, `const` constructors, provider/riverpod/bloc for state, GoRouter for navigation
- Ask first: `StatefulWidget` for ephemeral state, custom `InheritedWidget`, platform channels
- Never: Use `StatefulWidget` when `StatelessWidget` suffices, ignore `const` constructors, use `BuildContext` across async gaps""",
}

CODE_EXAMPLES["swift"] = {
    "examples": """## Code Examples

Good:
```swift
struct User: Codable, Identifiable {
    let id: Int
    let name: String
    let email: String?
}

@MainActor
class UserViewModel: ObservableObject {
    @Published var users: [User] = []

    func fetchUsers() async throws {
        let (data, _) = try await URLSession.shared.data(from: url)
        users = try JSONDecoder().decode([User].self, from: data)
    }
}
```

Bad:
```swift
class User {
    var id: Int = 0
    var name: String = ""
    var email: String = ""
}

class UserViewModel: NSObject {
    var users: [User] = []

    func fetchUsers() {
        URLSession.shared.dataTask(with: url) { data, _, _ in
            self.users = try! JSONDecoder().decode([User].self, from: data!)
        }.resume()
    }
}
```""",
    "boundaries": """## Boundaries

- Always: Use `struct` for models, `Codable` for JSON, `async/await` over completion handlers, value types by default
- Ask first: Classes for reference semantics, `@objc` interop, manual KVO
- Never: Use `try!` without justification, force-unwrap optionals, ignore SwiftLint warnings""",
}

# ── Batch 10: Infrastructure ───────────────────────────────────

CODE_EXAMPLES["docker"] = {
    "examples": """## Code Examples

Good:
```dockerfile
FROM python:3.12-slim AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
HEALTHCHECK --interval=30s CMD python -c "import requests; requests.get('http://localhost:8000/health')"
CMD ["python", "main.py"]
```

Bad:
```dockerfile
FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```""",
    "boundaries": """## Boundaries

- Always: Use multi-stage builds, pin base image versions, `.dockerignore`, HEALTHCHECK
- Ask first: `--squash` layers, custom base images, `ADD` over `COPY`
- Never: Use `:latest` tag, run as root, ignore `.dockerignore`, hardcode secrets in build args""",
}

CODE_EXAMPLES["bash"] = {
    "examples": """## Code Examples

Good:
```bash
#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/backups}"
mkdir -p "$BACKUP_DIR"

for db in "$@"; do
    pg_dump "$db" > "${BACKUP_DIR}/${db}.sql"
done
```

Bad:
```bash
#!/bin/bash
BACKUP_DIR=/backups

for db in $@; do
    pg_dump $db > $BACKUP_DIR/$db.sql
done
```""",
    "boundaries": """## Boundaries

- Always: Use `set -euo pipefail`, quote all variable expansions, `[[ ]]` over `[ ]`, use functions for reusable logic
- Ask first: `eval`, process substitution on non-Bash shells, associative arrays
- Never: Parse `ls` output, use backticks over `$()`, ignore exit codes of commands""",
}

CODE_EXAMPLES["cplusplus"] = {
    "examples": """## Code Examples

Good:
```cpp
#include <memory>
#include <vector>

class UserRepository {
public:
    auto findById(int id) -> std::unique_ptr<User> {
        auto user = std::make_unique<User>();
        user->id = id;
        return user;
    }
};
```

Bad:
```cpp
#include <vector>

class UserRepository {
public:
    User* findById(int id) {
        User* user = new User();
        user->id = id;
        return user;
    }
};
```""",
    "boundaries": """## Boundaries

- Always: Use RAII for resource management, smart pointers over raw, `constexpr` where applicable, C++20/23 features
- Ask first: Raw pointers for non-owning access, `reinterpret_cast`, manual memory management
- Never: Use `new`/`delete` manually, C-style casts, `#define` for constants (use `constexpr`/`const`)""",
}

# ── Batch 11: Remaining ────────────────────────────────────────

CODE_EXAMPLES["astro"] = {
    "examples": """## Code Examples

Good:
```astro
---
import Layout from '../layouts/Base.astro';
const { posts } = Astro.props;
---

<Layout title="Blog">
  {posts.map(post => (
    <article>
      <h2><a href={`/posts/${post.slug}`}>{post.title}</a></h2>
    </article>
  ))}
</Layout>
```

Bad:
```astro
---
const posts = await fetch('https://api.example.com/posts').then(r => r.json());
---

<html>
<body>
  {posts.map(post => <div><h2>{post.title}</h2></div>)}
</body>
</html>
```""",
    "boundaries": """## Boundaries

- Always: Use `.astro` components for static content, islands architecture for interactivity, content collections for blogs
- Ask first: Client-side JavaScript for static content, custom integrations, SSR mode
- Never: Fetch data in component template (use `Astro.props`), use client directives unnecessarily""",
}

CODE_EXAMPLES["django"] = {
    "examples": """## Code Examples

Good:
```python
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name
```

Bad:
```python
class product(models.Model):
    product_name = models.TextField()
    Product_Price = models.FloatField()
```""",
    "boundaries": """## Boundaries

- Always: Use model verbose names, write migrations for schema changes, use `related_name` on ForeignKey fields
- Ask first: Use raw SQL, modify the user model, change existing migration files
- Never: Use `null=False` on CharField/TextField, store files in database, commit with unresolved migrations""",
}

CODE_EXAMPLES["elasticsearch"] = {
    "examples": """## Code Examples

Good:
```json
PUT /products
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "price": { "type": "float" },
      "created_at": { "type": "date" }
    }
  },
  "aliases": { "products_search": {} }
}
```

Bad:
```json
PUT /products
{
  "mappings": {
    "dynamic": true
  }
}
```""",
    "boundaries": """## Boundaries

- Always: Plan index mappings carefully, use index aliases for zero-downtime reindexing, set appropriate shard count
- Ask first: Dynamic mapping, parent/child relationships, custom analyzers
- Never: Use Elasticsearch as primary database, disable replica shards in production, ignore cluster health""",
}

CODE_EXAMPLES["javascript"] = {
    "examples": """## Code Examples

Good:
```javascript
const fetchUsers = async () => {
  const response = await fetch('/api/users');
  const data = await response.json();
  return data.map(({ id, name }) => ({ id, name }));
};
```

Bad:
```javascript
function fetchUsers() {
  return fetch('/api/users').then(function(response) {
    return response.json();
  }).then(function(data) {
    return data.map(function(user) {
      return { id: user.id, name: user.name };
    });
  });
}
```""",
    "boundaries": """## Boundaries

- Always: Use `const` by default, `let` only when reassigning, `===` over `==`, `async/await` over raw promises
- Ask first: `var`, CommonJS (`require`), mutation patterns over immutability
- Never: Use `==` for comparison, rely on implicit semicolons, mutate function parameters""",
}

CODE_EXAMPLES["python"] = {
    "examples": """## Code Examples

Good:
```python
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    email: str


def fetch_user(user_id: int) -> User | None:
    return User.objects.filter(id=user_id).first()
```

Bad:
```python
def get_user_data(id):
    data = db.query("SELECT * FROM users WHERE id = " + str(id))
    return data
```""",
    "boundaries": """## Boundaries

- Always: Use type hints, write tests, use f-strings
- Ask first: Remove existing functionality, modify public API signatures
- Never: Use wildcard imports (`from x import *`), catch bare exceptions, commit without running lint""",
}
