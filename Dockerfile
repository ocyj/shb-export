
FROM mcr.microsoft.com/playwright/dotnet:v1.50.0-noble AS build

WORKDIR /src

# Copy the solution file and project files
COPY ShbExport.sln ./

COPY src/ src/

# Restore NuGet packages
RUN dotnet restore

# Publish the console app in Release configuration
RUN dotnet publish src/ShbExport.Console/ShbExport.Console.csproj -c Release -o /app

# Use the same Playwright image as the runtime
FROM mcr.microsoft.com/playwright/dotnet:v1.50.0-noble AS runtime
WORKDIR /app

# Copy the published output from the build stage
COPY --from=build /app .

# Set the entrypoint to run the console application
ENTRYPOINT ["dotnet", "ShbExport.Console.dll"]