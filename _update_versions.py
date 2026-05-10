"""Update tech_config.json with version_source for all technologies."""

import json

with open("tech_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

sources = {
    "angular": "npm:@angular/core",
    "aspnetcore": "github:dotnet/aspnetcore",
    "astro": "npm:astro",
    "bash": "",
    "blazor": "github:dotnet/aspnetcore",
    "cplusplus": "",
    "csharp": "github:dotnet/roslyn",
    "css": "",
    "daisyui": "npm:daisyui",
    "dart": "github:dart-lang/sdk",
    "django": "pypi:django",
    "docker": "github:moby/moby",
    "elasticsearch": "github:elastic/elasticsearch",
    "express": "npm:express",
    "fastapi": "pypi:fastapi",
    "flask": "pypi:flask",
    "flutter": "github:flutter/flutter",
    "go": "github:golang/go",
    "html": "",
    "java": "github:openjdk/jdk",
    "javascript": "",
    "jest": "npm:jest",
    "jquery": "npm:jquery",
    "kotlin": "github:JetBrains/kotlin",
    "laravel": "github:laravel/laravel",
    "mariadb": "github:mariadb/server",
    "mongodb": "github:mongodb/mongo",
    "mysql": "github:mysql/mysql-server",
    "nestjs": "npm:@nestjs/core",
    "next.js": "npm:next",
    "node": "github:nodejs/node",
    "nuxt.js": "npm:nuxt",
    "php": "github:php/php-src",
    "playwright": "npm:@playwright/test",
    "postgresql": "github:postgres/postgres",
    "python": "github:python/cpython",
    "rails": "rubygems:rails",
    "react": "npm:react",
    "redis": "github:redis/redis",
    "ruby": "github:ruby/ruby",
    "rust": "github:rust-lang/rust",
    "sass": "npm:sass",
    "scss": "npm:sass",
    "spring": "github:spring-projects/spring-framework",
    "springboot": "github:spring-projects/spring-boot",
    "sqlite": "",
    "svelte": "npm:svelte",
    "swift": "github:swiftlang/swift",
    "tailwind": "npm:tailwindcss",
    "typescript": "npm:typescript",
    "uv": "pypi:uv",
    "vite": "npm:vite",
    "vitest": "npm:vitest",
    "vue": "npm:vue",
}

for key, entry in config.items():
    new_source = sources.get(key, "")
    if new_source != entry.get("version_source", ""):
        print(f'{key}: "{entry.get("version_source", "")}" -> "{new_source}"')
        entry["version_source"] = new_source

with open("tech_config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("\nDone!")
