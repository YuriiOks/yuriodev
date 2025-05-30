# 1. Base image for installing dependencies and building
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package.json and lock file
COPY package.json yarn.lock* package-lock.json* ./

# Install dependencies
RUN if [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    else npm install; fi

# Copy the rest of the application code
COPY . .

# Build the Next.js application
RUN npm run build

# 2. Base image for running the application (smaller image)
FROM node:18-alpine
WORKDIR /app

# Copy built assets from builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
# Ensure node_modules are also copied if start script needs them (Next.js standalone output might not)
# If using Next.js standalone output (recommended for production), these node_modules might not be needed here.
# For now, let's assume a standard `next start` which might need some production dependencies.
COPY --from=builder /app/node_modules ./node_modules


# Expose port 3000 (Next.js default)
EXPOSE 3000

# Command to run the application
# Use "next start" which is the standard way to run a production Next.js app
# Ensure your package.json's "start" script is `next start`
CMD ["npm", "start"]
